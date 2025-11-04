# Admin Dashboard Database Migration

Add the following columns to your `violation_reports` table in Supabase:

```sql
-- Add admin approval columns
ALTER TABLE violation_reports 
ADD COLUMN IF NOT EXISTS admin_reviewed BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS admin_approved BOOLEAN DEFAULT FALSE;

-- Add index for faster queries on admin dashboard
CREATE INDEX IF NOT EXISTS idx_admin_reviewed ON violation_reports(admin_reviewed);
CREATE INDEX IF NOT EXISTS idx_admin_approved ON violation_reports(admin_approved);
CREATE INDEX IF NOT EXISTS idx_needs_verification ON violation_reports(needs_manual_verification);
```

These columns enable:
- `admin_reviewed`: Whether an admin has reviewed the report (approved or rejected)
- `admin_approved`: Whether the report was approved (true) or rejected (false)
- Indexes for optimized filtering and queries

The system will continue to work without these columns, but approval functionality will be limited until migration is complete.
