
import typing as ty
import logging

from qiskit import QuantumCircuit
from qiskit.circuit.quantumregister import Qubit

from Utils.Parallel_mapping.mapping.gates import (
    TwoQubitGate,
    SwapTwoQubitGate,
    BridgeTwoQubitGate,
)
from Utils.Parallel_mapping.hardware.IBMQHardwareArchitecture import (
    IBMQHardwareArchitecture,
)
from Utils.Parallel_mapping.mapping._mapping_to_str import mapping_to_str_multiple

logger = logging.getLogger("swap")


def get_all_swap_candidates(
    gates_to_resolve: ty.List,
    hardware: IBMQHardwareArchitecture,
    partition: ty.List,
    current_mapping: ty.Dict[Qubit, int],
    initial_mapping: ty.Dict[Qubit, int],
    explored_mappings: ty.Set[str],
    merged_partition = None,
) -> ty.List[SwapTwoQubitGate]:
    # First compute all the qubits involved in the given layer
    qubits_involved_in_front_layer = set()
    if isinstance(gates_to_resolve, list):
        for op in gates_to_resolve:
            qubits_involved_in_front_layer.update(op.qargs)
    else:
        for op in gates_to_resolve.ops:
            qubits_involved_in_front_layer.update(op.qargs)
    inverse_mapping = {val: key for key, val in current_mapping.items()}
    # Then for all the possible links that involve at least one of the qubits used by
    # the gates in the given layer, add this link as a possible SWAP.
    all_swaps = list()
    for involved_qubit in qubits_involved_in_front_layer:
        qubit_index = current_mapping[involved_qubit]
        # For all the links that involve the current qubit.
        for source, sink in hardware.out_edges(qubit_index):
            if source not in partition or sink not in partition:
                continue
            two_qubit_gate = SwapTwoQubitGate(
                inverse_mapping[source], inverse_mapping[sink]
            )

            # Check that the mapping has not already been explored in this
            # SWAP-insertion pass.
            if merged_partition == None:
                merged_partition = partition
            if (
                mapping_to_str_multiple(two_qubit_gate.update_mapping(current_mapping))
                not in explored_mappings
            ):
                all_swaps.append(two_qubit_gate)
    return all_swaps

def get_all_bridge_candidates(
    gates_to_resolve: ty.List,
    hardware: IBMQHardwareArchitecture,
    partition: ty.List,
    current_mapping: ty.Dict[Qubit, int],
    initial_mapping: ty.Dict[Qubit, int],
    trans_mapping: ty.Dict[Qubit, int],
    explored_mappings: ty.Set[str],
    merged_partition = None,
) -> ty.List[BridgeTwoQubitGate]:
    all_bridges = []
    inverse_mapping = {val: key for key, val in initial_mapping.items()}
    inverse_trans_mapping = {val: key for key, val in trans_mapping.items()}
    # First compute all the qubits involved in the given layer
    if not isinstance(gates_to_resolve, list):
        gates_to_resolve = list(gates_to_resolve.ops)

    for op in gates_to_resolve:
        if len(op.qargs) < 2:
            # We just pass 1 qubit gates because they do not participate in the
            # Bridge operation
            continue
        if len(op.qargs) != 2:
            logger.warning("A 3-qubit or more gate has been found in the circuit.")
            continue

        control, target = op.qargs

        control_index = initial_mapping[inverse_trans_mapping[initial_mapping[control]]]
        target_index = initial_mapping[inverse_trans_mapping[initial_mapping[target]]]
        # For each qubit q linked with control, check if target is linked with q.
        for _, potential_middle_index in hardware.out_edges(control_index):
            if potential_middle_index not in partition:
                continue
            for _, potential_target_index in hardware.out_edges(potential_middle_index):
                if potential_target_index == target_index:
                    two_qubit_gate = BridgeTwoQubitGate(
                        inverse_trans_mapping[initial_mapping[control]],
                        inverse_mapping[potential_middle_index],
                        inverse_trans_mapping[initial_mapping[target]],
                    )
                    if merged_partition == None:
                        merged_partition = partition
                    # Check that the mapping has not already been explored in this
                    # SWAP-insertion pass.
                    if (
                        mapping_to_str_multiple(two_qubit_gate.update_mapping(current_mapping))
                        not in explored_mappings
                    ):
                        all_bridges.append(two_qubit_gate)

    return all_bridges


def get_all_swap_bridge_candidates(
    gates_to_resolve: ty.List,
    hardware: IBMQHardwareArchitecture,
    partition: ty.List,
    current_mapping: ty.Dict[Qubit, int],
    initial_mapping: ty.Dict[Qubit, int],
    trans_mapping: ty.Dict[Qubit, int],
    explored_mappings: ty.Set[str],
    merged_partition = None,
) -> ty.List[TwoQubitGate]:
    swap_candidates = get_all_swap_candidates(
        gates_to_resolve, hardware, partition, current_mapping, initial_mapping, explored_mappings, merged_partition
    )
    bridge_candidates = get_all_bridge_candidates(
        gates_to_resolve, hardware, partition, current_mapping, initial_mapping, trans_mapping, explored_mappings, merged_partition
    )
    return swap_candidates + bridge_candidates


def change_mapping(
    start_mapping: ty.Dict[Qubit, int],
    final_mapping: ty.Dict[Qubit, int],
    circuit: QuantumCircuit,
) -> None:
    reverse_initial_mapping = {val: key for key, val in start_mapping.items()}
    reverse_final_mapping = {val: key for key, val in final_mapping.items()}
    # For each qubit index, exchange the qubit currently occupying the position (
    # given by start_mapping) with the qubit that should be there at the end (given
    # by final_mapping) and update the current mapping. The last swap is not needed
    # because the qubit should already be in the right place.
    for i in range(len(reverse_initial_mapping) - 1):
        s1, s2 = reverse_initial_mapping[i], reverse_final_mapping[i]
        if s1 != s2:
            circuit.swap(s1, s2)
            # Reflect the SWAP on the current mapping
            start_mapping[s1], start_mapping[s2] = start_mapping[s2], start_mapping[s1]
            reverse_initial_mapping = {val: key for key, val in start_mapping.items()}
