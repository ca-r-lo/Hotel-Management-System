# Messages Privacy Fix

## Problem
Messages were being shown to all users instead of being personal between sender and recipient. For example, the Department Manager could see messages between Owner and Purchase Admin.

## Root Causes
1. **Database Schema Issue**: The `messages` table was missing necessary columns (`sender_id`, `recipient_id`, `category`, `is_read`)
2. **Timing Issue**: The MessagesController was initialized before user login, causing it to use a default user_id (1) instead of the actual logged-in user's ID

## Solution

### 1. Updated Database Schema
Updated the `messages` table in `/models/purchase.py` to include:

**For MariaDB:**
```sql
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    category VARCHAR(64) DEFAULT 'General',
    title VARCHAR(255),
    body TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
)
```

**For SQLite:**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    category TEXT DEFAULT 'General',
    title TEXT,
    body TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
)
```

### 2. Fixed Timing Issue
**Problem**: MessagesController was initialized in DashboardWindow's `__init__` method, before user login, causing it to always use `user_id=1`.

**Solution**: 
- Modified `MessagesController.__init__()` to NOT load messages during initialization
- Updated `DashboardWindow.switch_page()` to refresh messages when user switches to the MESSAGES page
- This ensures the correct logged-in user's ID is used when loading messages

**Changes in `/views/dashboard.py`:**
```python
def switch_page(self, index, title):
    # ... existing code ...
    
    # Refresh messages when switching to messages page
    if title == "MESSAGES" and self.current_user:
        # Update the current user ID and refresh messages
        self.messages_ctrl.current_user_id = self.messages_ctrl.get_current_user_id()
        self.messages_ctrl.refresh_messages()
```

**Changes in `/controllers/messages_controller.py`:**
```python
def __init__(self, view, model, dashboard):
    # ... existing code ...
    
    # Don't load messages here - they will be loaded when the user switches to the messages page
    # (removed: self.refresh_messages())
```

### 3. Message Filtering Logic
The `MessageModel.list_messages(user_id)` method filters messages correctly:

```python
WHERE m.recipient_id = user_id OR m.sender_id = user_id
```

This ensures users only see:
- Messages they sent (where they are the sender)
- Messages sent to them (where they are the recipient)

### 4. Migration Script
Created `migrate_messages_table.py` to update existing databases without manual SQL commands.

## Result
✅ Messages are now **completely private** between sender and recipient
✅ Messages are loaded with the correct user ID after login
✅ Department Manager can only see messages sent to/from them
✅ Owner and Purchase Admin messages are private to them only
✅ Each user has their own personal inbox and sent items

## Testing
1. Login as different users (Owner, Purchase Admin, Department Manager, etc.)
2. Send messages between users
3. Verify that only the sender and recipient can see each message
4. Other users should not see messages they're not part of
5. Switch between users and verify messages are correctly filtered
