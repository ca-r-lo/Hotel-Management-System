# Requests Feature Implementation

## Overview
The Requests feature allows Department users to request stock items from the Purchase Admin.

## Database Schema

### `requests` Table
- `id` - Auto-increment primary key
- `department` - Department name (e.g., "Housekeeping", "Kitchen")
- `requested_by` - Name of the user who made the request
- `item_name` - Name of the requested item
- `quantity` - Amount requested
- `unit` - Unit of measurement (e.g., "pcs", "boxes")
- `reason` - Text explanation for the request
- `status` - Current status: "Pending", "Approved", "Rejected", "Archived"
- `created_at` - Timestamp when request was created
- `updated_at` - Timestamp when request was last updated
- `notes` - Additional notes (from Purchase Admin)

## Features

### For Department Users
1. **Send Request**: Create new stock requests with:
   - Item name
   - Quantity
   - Unit
   - Reason/justification

2. **View Requests**: See all requests from their department with:
   - Item details
   - Status (color-coded)
   - Date created
   - Requester name

3. **Delete Requests**: Remove requests they created

4. **Archive Toggle**: View archived vs active requests

### For Purchase Admin/Owner
- Can view ALL requests from all departments
- Can see which department made each request
- Can approve/reject requests (status management)
- Can add notes to requests

## Request Status Flow
1. **Pending** (Yellow) - Newly created request
2. **Approved** (Green) - Purchase Admin approved the request
3. **Rejected** (Gray) - Purchase Admin rejected the request
4. **Archived** (Gray) - Request has been archived

## UI Components

### Send Request Dialog
- Item Name input field
- Quantity spin box
- Unit input field
- Reason text area
- Cancel and Send buttons

### Request Card
- Item name and quantity (bold header)
- Department and requester info
- Status with color coding and date
- Delete button (trash icon)

## Code Structure

### Models
- `models/request.py` - RequestModel class with database operations:
  - `create_table()` - Initialize database table
  - `create_request()` - Create new request
  - `get_requests_by_department()` - Get department-specific requests
  - `get_all_requests()` - Get all requests (for admins)
  - `update_status()` - Change request status
  - `delete_request()` - Remove a request

### Views
- `views/requests.py`:
  - `SendRequestDialog` - Dialog for creating requests
  - `RequestsPage` - Main requests page with list

### Controllers
- `controllers/requests_controller.py`:
  - `RequestsController` - Handles all request operations
  - Button click handlers
  - Request list management
  - User info management

## Integration
- Integrated into dashboard navigation
- User info (name, role, department) passed from login
- Requests filtered by department for Department users
- All requests shown for Purchase Admin/Owner

## Next Steps
1. Implement request approval workflow for Purchase Admin
2. Add email/notification system for new requests
3. Implement sorting options (by date, status, department)
4. Add request editing capability
5. Add bulk operations (approve multiple, archive multiple)
6. Generate reports from requests data
