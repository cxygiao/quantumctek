
import typing as ty
from copy import copy
import logging

import numpy

from qiskit.circuit.quantumregister import Qubit
from qiskit.circuit import Gate, QuantumRegister
from qiskit.circuit.library.standard_gates.swap import SwapGate
from qiskit.circuit.library.standard_gates.x import CXGate

from qiskit.dagcircuit.dagcircuit import DAGCircuit, DAGNode

from Utils.Parallel_mapping.mapping.layer import QuantumLayer
from Utils.Parallel_mapping.hardware.IBMQHardwareArchitecture import (
    IBMQHardwareArchitecture,
)

logger = logging.getLogger("gates")


class _BridgeGate(Gate):
    """Bridge gate."""

    def __init__(self):
        """Create new Bridge gate."""
        super().__init__("bridge", 3, [])

    def _define(self):
        """
        gate bridge a,b,c { cx a,b; cx b,c; cx a,b; cx b,c; }
        """

        definition = []
        q = QuantumRegister(3, "q")
        rule = [
            (CXGate(), [q[0], q[1]], []),
            (CXGate(), [q[1], q[2]], []),
            (CXGate(), [q[0], q[1]], []),
            (CXGate(), [q[1], q[2]], []),
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def control(self, num_ctrl_qubits=1, label=None, **kwargs):
        """Controlled version of this gate.

        Args:
            num_ctrl_qubits (int): number of control qubits.
            label (str or None): An optional label for the gate [Default: None]

        Returns:
            ControlledGate: controlled version of this gate.
        """
        return super().control(num_ctrl_qubits=num_ctrl_qubits, label=label, **kwargs)

    def inverse(self):
        """Invert this gate."""
        return _BridgeGate()  # self-inverse

    def to_matrix(self):
        """Return a Numpy.array for the Swap gate."""
        return numpy.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0],
            ],
            dtype=complex,
        )


def get_updated_mapping(
    current_mapping: ty.Dict[Qubit, int],
    swap: ty.Tuple[Qubit, Qubit]
) -> ty.Dict[Qubit, int]:
    source, sink = swap
    new_mapping = copy(current_mapping)
    new_mapping[source], new_mapping[sink] = new_mapping[sink], new_mapping[source]
    return new_mapping


class TwoQubitGate:
    def __init__(self, left: Qubit, right: Qubit):
        self._left: Qubit = left
        self._right: Qubit = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def update_mapping(
        self,
        previous_mapping: ty.Dict[Qubit, int],
    ) -> ty.Dict[Qubit, int]:
        raise NotImplementedError()

    def apply(self,
              dag_circuit: DAGCircuit,
              front_layer: QuantumLayer,
              initial_mapping: ty.Dict[Qubit, int],
              trans_mapping: ty.Dict[Qubit, int],
              ):
        raise NotImplementedError()

    def implements_operation(self,
                             op,
                             initial_mapping: ty.Dict[Qubit, int],
                             trans_mapping: ty.Dict[Qubit,int],
                             ) -> bool:
        raise NotImplementedError()

    def cost(self, hardware, mapping, distance_matrix,) -> float:
        raise NotImplementedError()


class SwapTwoQubitGate(TwoQubitGate):
    def __init__(self, left, right):
        super().__init__(left, right)

    def update_mapping(
        self,
        previous_mapping: ty.Dict[Qubit, int],
    ) -> ty.Dict[Qubit, int]:
        return get_updated_mapping(previous_mapping,(self.left, self.right))

    def apply(self,
              dag_circuit: DAGCircuit,
              front_layer: QuantumLayer,
              initial_mapping: ty.Dict[Qubit, int],
              trans_mapping: ty.Dict[Qubit, int],
    ):
        dag_circuit.apply_operation_back(SwapGate(), [self.left, self.right])

    def implements_operation(self,
                             op,
                             initial_mapping: ty.Dict[Qubit, int],
                             trans_mapping: ty.Dict[Qubit, int],
                             ) -> bool:
        # The SWAP gate does not implement an operation of the quantum circuit,
        # it is an additional operation changing the mapping.
        return False

    def cost(
            self, hardware: IBMQHardwareArchitecture,
            mapping: ty.Dict[Qubit, int],
            distance_matrix: numpy.ndarray,
    ) -> float:
        a = distance_matrix.item(mapping[self.left], mapping[self.right])

        b = distance_matrix.item(mapping[self.right], mapping[self.left])

        return a + b + min(a, b)


class BridgeTwoQubitGate(TwoQubitGate):
    def __init__(self, left, middle, right):
        super().__init__(left, right)
        self._middle = middle

    def update_mapping(
        self,
        previous_mapping: ty.Dict[Qubit, int],
    ) -> ty.Dict[Qubit, int]:
        # Do nothing, we do not change the mapping with a Bridge gate.
        return previous_mapping

    @property
    def middle(self):
        return self._middle

    def apply(self,
              dag_circuit: DAGCircuit,
              front_layer: QuantumLayer,
              initial_mapping: ty.Dict[Qubit, int],
              #current_mapping: ty.Dict[Qubit, int],
              trans_mapping: ty.Dict[Qubit, int],
              ):
        dag_circuit.apply_operation_back(CXGate(), [self.middle, self.right])
        dag_circuit.apply_operation_back(CXGate(), [self.left, self.middle])
        dag_circuit.apply_operation_back(CXGate(), [self.middle, self.right])
        dag_circuit.apply_operation_back(CXGate(), [self.left, self.middle])
        # dag_circuit.apply_operation_back(
        #     _BridgeGate(), [self.left, self.middle, self.right]
        # )
        # Do not forget to remove the CNOT gate from self.left to self.right from the
        # front layer.
        op_to_remove: ty.Optional[DAGNode] = None
        for op in front_layer.ops:
            q1, q2 = initial_mapping[op.qargs[0]], initial_mapping[op.qargs[1]]
            if (
                len(op.qargs) == 2
                and q1 == trans_mapping[self.left]
                and q2 == trans_mapping[self.right]
            ):
                op_to_remove = op
        if op_to_remove is None:
            logger.warning(
                "Could not find a corresponding CNOT gate to remove with "
                "Bridge usage. Resulting circuit will likely be wrong."
            )
        else:
            front_layer.remove_operation(op_to_remove)

    def implements_operation(self,
                             op,
                             initial_mapping: ty.Dict[Qubit, int],
                             trans_mapping: ty.Dict[Qubit, int],
                             ) -> bool:
        # The Bridge gate implements a CNOT from the circuit
        q1, q2 = initial_mapping[op.qargs[0]], initial_mapping[op.qargs[1]]
        return (
                len(op.qargs) == 2
                and q1 == trans_mapping[self.left]
                and q2 == trans_mapping[self.right]
        )

    def cost(
            self,
            hardware: IBMQHardwareArchitecture,
            mapping: ty.Dict[Qubit, int],
            distance_matrix: numpy.ndarray,
    ) -> float:
        a = distance_matrix.item(mapping[self.left], mapping[self.middle])
        b = distance_matrix.item(mapping[self.middle], mapping[self.right])
        return 2 * (a + b)
