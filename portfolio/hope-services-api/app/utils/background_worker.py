import threading
import time
import logging
from queue import Queue
from app import db
from app.models import Order, JobStatus, IdempotencyKey
from datetime import datetime

logger = logging.getLogger(__name__)

class BackgroundWorker:
    def __init__(self):
        self.job_queue = Queue()
        self.jobs = {}  # job_id -> status
        self.running = False
        self.worker_thread = None
    
    def start(self):
        """Start the background worker thread"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logger.info("Background worker started")
    
    def stop(self):
        """Stop the background worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("Background worker stopped")
    
    def enqueue_job(self, job_type, order_id, job_data=None):
        """Enqueue a job and return job_id"""
        job_id = IdempotencyKey.generate_key()
        
        job = {
            'job_id': job_id,
            'job_type': job_type,
            'order_id': order_id,
            'status': 'queued',
            'created_at': datetime.utcnow(),
            'data': job_data or {},
        }
        
        self.jobs[job_id] = job
        self.job_queue.put(job)
        
        # Store in database (need app context)
        from flask import current_app
        import json
        with current_app.app_context():
            job_status = JobStatus(
                job_id=job_id,
                job_type=job_type,
                status='queued',
                order_id=order_id,
                metadata=json.dumps(job_data) if job_data else None
            )
            db.session.add(job_status)
            db.session.commit()
        
        logger.info(f"Job {job_id} ({job_type}) enqueued for order {order_id}")
        return job_id
    
    def get_job_status(self, job_id):
        """Get status of a job"""
        # Check in-memory first
        if job_id in self.jobs:
            return self.jobs[job_id]
        
        # Check database (need app context)
        from flask import has_app_context
        if has_app_context():
            job_status = JobStatus.query.filter_by(job_id=job_id).first()
            if job_status:
                return {
                    'job_id': job_status.job_id,
                    'job_type': job_status.job_type,
                    'status': job_status.status,
                    'order_id': job_status.order_id,
                    'created_at': job_status.created_at.isoformat() if job_status.created_at else None,
                    'completed_at': job_status.completed_at.isoformat() if job_status.completed_at else None,
                    'error': job_status.error,
                }
        
        return None
    
    def _worker_loop(self):
        """Main worker loop"""
        while self.running:
            try:
                # Get job from queue (non-blocking with timeout)
                try:
                    job = self.job_queue.get(timeout=1)
                except:
                    continue
                
                job_id = job['job_id']
                job_type = job['job_type']
                order_id = job['order_id']
                
                # Update status to running
                self._update_job_status(job_id, 'running')
                logger.info(f"Job {job_id} ({job_type}) started for order {order_id}")
                
                try:
                    # Execute job
                    if job_type == 'send_receipt':
                        self._send_receipt(order_id)
                    elif job_type == 'inventory_sync':
                        self._sync_inventory(order_id)
                    else:
                        raise ValueError(f"Unknown job type: {job_type}")
                    
                    # Mark as completed
                    self._update_job_status(job_id, 'done')
                    logger.info(f"Job {job_id} ({job_type}) completed for order {order_id}")
                    
                except Exception as e:
                    # Mark as failed
                    self._update_job_status(job_id, 'failed', str(e))
                    logger.error(f"Job {job_id} ({job_type}) failed: {str(e)}")
                
                self.job_queue.task_done()
                
            except Exception as e:
                logger.error(f"Worker loop error: {str(e)}")
                time.sleep(1)
    
    def _update_job_status(self, job_id, status, error=None):
        """Update job status in memory and database"""
        # Update in-memory
        if job_id in self.jobs:
            self.jobs[job_id]['status'] = status
            if status == 'done':
                self.jobs[job_id]['completed_at'] = datetime.utcnow()
            if error:
                self.jobs[job_id]['error'] = error
        
        # Update database (need app context)
        try:
            from flask import current_app
            with current_app.app_context():
                job_status = JobStatus.query.filter_by(job_id=job_id).first()
                if job_status:
                    job_status.status = status
                    if status == 'done':
                        job_status.completed_at = datetime.utcnow()
                    if error:
                        job_status.error = error
                    db.session.commit()
        except Exception as e:
            logger.error(f"Error updating job status in DB: {str(e)}")
            try:
                db.session.rollback()
            except:
                pass
    
    def _send_receipt(self, order_id):
        """Simulate sending receipt email"""
        time.sleep(0.5)  # Simulate work
        logger.info(f"Receipt sent for order {order_id}")
    
    def _sync_inventory(self, order_id):
        """Simulate inventory synchronization"""
        time.sleep(0.5)  # Simulate work
        
        # Update inventory quantities (need app context)
        from flask import current_app
        with current_app.app_context():
            order = Order.query.get(order_id)
            if order:
                for item in order.items:
                    inventory_item = item.inventory_item
                    if inventory_item.quantity >= item.quantity:
                        inventory_item.quantity -= item.quantity
                db.session.commit()
        
        logger.info(f"Inventory synced for order {order_id}")

# Global worker instance
background_worker = BackgroundWorker()

