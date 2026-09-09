# LibreChat MongoDB Setup Guide

## Overview
This configuration enables LibreChat to store conversation history and user data in MongoDB.

## Database Information
- **Database Host**: MongoDB Atlas
- **Cluster**: cluster0.c5czxzo.mongodb.net
- **User**: long1029_db_user
- **Database Name**: librechat

## Environment Variables

Add the following to your `.env` file:

```
MONGODB_URI=mongodb+srv://long1029_db_user:<db_password>@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
DB_NAME=librechat
```

**Important**: Replace `<db_password>` with your actual MongoDB password.

## Features Enabled

With MongoDB configured, LibreChat will support:
- Conversation History Storage
- User Preferences
- Chat Sessions
- User Authentication
- API Keys Management

## Connection Testing

Run the configuration script to verify MongoDB settings:

```bash
python mongodb_config.py
```

## LibreChat Configuration

Add these variables to your LibreChat deployment environment:

```
MONGODB_URI=mongodb+srv://long1029_db_user:<password>@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
DB_NAME=librechat
DEBUG_LOGGING=true
```

## Troubleshooting

1. **Connection Timeout**: 
   - Verify MongoDB username and password
   - Check IP whitelist in MongoDB Atlas (should be 0.0.0.0/0)

2. **Authentication Failed**:
   - Ensure correct password is used
   - Verify user exists in MongoDB Atlas

3. **Database Not Found**:
   - Database will be created automatically on first connection
   - Ensure DB_NAME variable is set

## Files

- `.env`: Configuration file with connection details
- `mongodb_config.py`: Configuration verification script
- `MONGODB_SETUP.md`: This setup guide

## Render Integration

For Render deployment, add these environment variables in the Render dashboard:

1. Go to: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
2. Settings > Environment Variables
3. Add:
   - MONGODB_URI
   - DB_NAME

## Security Notes

- Never commit `.env` file to version control
- Rotate MongoDB password regularly
- Use strong passwords for MongoDB users
- Enable IP whitelisting in MongoDB Atlas

## Support

For LibreChat MongoDB setup issues, refer to:
https://github.com/danny-avila/LibreChat/wiki/MongoDB-Setup