# Database Schema Migration Required

## New Fields Added to `violation_reports` Table

The following fields have been added to support enhanced analysis:

### Fields to Add:

```sql
-- Add license plate confidence score
ALTER TABLE violation_reports 
ADD COLUMN license_plate_confidence FLOAT DEFAULT 0;

-- Add location detection fields
ALTER TABLE violation_reports 
ADD COLUMN is_india_location BOOLEAN DEFAULT TRUE;

ALTER TABLE violation_reports 
ADD COLUMN location_confidence FLOAT DEFAULT 0;
```

### Migration Steps:

1. Connect to your Supabase project
2. Go to SQL Editor
3. Run the above SQL commands
4. Verify the columns are added by checking the table structure

### Why These Fields?

- **`license_plate_confidence`**: Tracks the confidence level of license plate detection (0-1). Low confidence plates (<0.7) won't be displayed in summaries to avoid false implications.

- **`is_india_location`**: Boolean flag indicating if the image appears to be from India based on visual cues (license plate format, vehicle types, road signs, etc.)

- **`location_confidence`**: Confidence score (0-1) for the location determination. If confidence is >0.99 that it's NOT India, a warning is displayed.

### Backward Compatibility:

- All fields have default values, so existing rows will automatically get:
  - `license_plate_confidence`: 0 (will require manual review)
  - `is_india_location`: TRUE (assumed to be India)
  - `location_confidence`: 0 (unknown)
