from typing import Tuple
from algopy import *
from algopy.arc4 import abimethod, Struct, UInt64 as ARC4UInt64, String as ARC4String


class BatchRecord(Struct):
    """Batch record structure"""
    producer: ARC4String  # Account address stored as base32-encoded string (58 chars)
    product_name: ARC4String
    origin_location: ARC4String
    harvest_date: ARC4UInt64
    status: ARC4UInt64
    ipfs_hash: ARC4String
    inspection_report_hash: ARC4String


class FoodSafetyApp(ARC4Contract):
    """Food Safety & Traceability application.

    Uses one box per `batch_id` to store a BatchRecord struct.
    """

    def __init__(self) -> None:
        # record contract creator
        self.creator = Txn.sender
        # BoxMap keyed by batch_id storing a BatchRecord for each batch
        self.batches = BoxMap(String, BatchRecord, key_prefix="batches")

    @abimethod()
    def create_batch(self, batch_id: String, producer_address: String, product_name: String, origin_location: String, harvest_date: UInt64, ipfs_hash: String) -> None:
        """Create a new batch. producer_address should be the account address string (58-char base32). Initial status = 0 (CREATED)."""
        assert not self.batches.maybe(batch_id)[1], "Batch already exists"
        
        record = BatchRecord(
            producer=ARC4String(producer_address),
            product_name=ARC4String(product_name),
            origin_location=ARC4String(origin_location),
            harvest_date=ARC4UInt64(harvest_date),
            status=ARC4UInt64(UInt64(0)),
            ipfs_hash=ARC4String(ipfs_hash),
            inspection_report_hash=ARC4String(String(""))
        )
        self.batches[batch_id] = record.copy()

    @abimethod()
    def inspect_batch(self, batch_id: String, inspection_report_hash: String, approved: UInt64) -> None:
        """Inspect a batch. Only allowed when status == CREATED (0). approved: non-zero -> APPROVED, zero -> REJECTED"""
        # Access maybe result directly to avoid mutable reference assignment
        assert self.batches.maybe(batch_id)[1], "Batch does not exist"
        current = self.batches.maybe(batch_id)[0].copy()

        assert current.status.native == UInt64(0), "Batch not in CREATED state"

        new_status = ARC4UInt64(UInt64(2)) if approved != UInt64(0) else ARC4UInt64(UInt64(3))
        updated = BatchRecord(
            producer=current.producer,
            product_name=current.product_name,
            origin_location=current.origin_location,
            harvest_date=current.harvest_date,
            status=new_status,
            ipfs_hash=current.ipfs_hash,
            inspection_report_hash=ARC4String(inspection_report_hash)
        )
        self.batches[batch_id] = updated.copy()

    @abimethod()
    def distribute_batch(self, batch_id: String) -> None:
        # Access maybe result directly to avoid mutable reference assignment
        assert self.batches.maybe(batch_id)[1], "Batch does not exist"
        current = self.batches.maybe(batch_id)[0].copy()
        assert current.status.native == UInt64(2), "Batch not APPROVED"
        updated = BatchRecord(
            producer=current.producer,
            product_name=current.product_name,
            origin_location=current.origin_location,
            harvest_date=current.harvest_date,
            status=ARC4UInt64(UInt64(4)),
            ipfs_hash=current.ipfs_hash,
            inspection_report_hash=current.inspection_report_hash
        )
        self.batches[batch_id] = updated.copy()

    @abimethod()
    def recall_batch(self, batch_id: String, reason_hash: String) -> None:
        assert Txn.sender == self.creator, "Only contract creator can recall"
        # Access maybe result directly to avoid mutable reference assignment
        assert self.batches.maybe(batch_id)[1], "Batch does not exist"
        current = self.batches.maybe(batch_id)[0].copy()
        updated = BatchRecord(
            producer=current.producer,
            product_name=current.product_name,
            origin_location=current.origin_location,
            harvest_date=current.harvest_date,
            status=ARC4UInt64(UInt64(5)),
            ipfs_hash=current.ipfs_hash,
            inspection_report_hash=ARC4String(reason_hash)
        )
        self.batches[batch_id] = updated.copy()

    @abimethod(readonly=True)
    def get_batch(self, batch_id: String) -> Tuple[String, String, String, String, UInt64, UInt64, String, String]:
        # Access maybe result directly to avoid mutable reference assignment
        assert self.batches.maybe(batch_id)[1], "Batch does not exist"
        current = self.batches.maybe(batch_id)[0].copy()
        # return (batch_id, producer_address_string, product_name, origin_location, harvest_date, status, ipfs_hash, inspection_report_hash)
        return (batch_id, current.producer.native, current.product_name.native, current.origin_location.native, current.harvest_date.native, current.status.native, current.ipfs_hash.native, current.inspection_report_hash.native)
