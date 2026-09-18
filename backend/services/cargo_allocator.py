"""
Cargo Allocator Service — Computes allocation figures, unallocated balances, and utilization ratios.
"""

from backend.models.decision_models import AllocationResult, VoyageProposalModel


class CargoAllocator:
    """Calculates allocation metrics and identifies capacity over-allocation."""

    @staticmethod
    def allocate(proposal: VoyageProposalModel) -> AllocationResult:
        capacity = max(proposal.vessel.capacity_dwt, 0.0001)
        cargo_qty = proposal.cargo.quantity_mt

        allocated = min(cargo_qty, capacity)
        unallocated = max(0.0, cargo_qty - capacity)
        utilization = cargo_qty / capacity
        over_capacity = cargo_qty > capacity

        return AllocationResult(
            allocated_mt=round(allocated, 2),
            unallocated_mt=round(unallocated, 2),
            capacity_dwt=round(capacity, 2),
            utilization_ratio=round(utilization, 4),
            over_capacity=over_capacity,
        )