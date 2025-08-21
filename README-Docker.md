# 🏁 FTQoin Racing Scanner - Docker Setup

A Mario Kart themed QR code scanner for VDV train tickets with improved passenger name extraction.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone or download the project
# Navigate to the project directory
cd /path/to/ftqoin-scanner

# Build and start the application
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -f Dockerfile.local -t ftqoin-scanner .

# Run the container
docker run -p 8000:8000 ftqoin-scanner
```

## 🌐 Access the Application

Once running, open your browser and go to:

- **Main Scanner**: http://localhost:8000/
- **Settings Page**: http://localhost:8000/settings/
- **Admin Panel**: http://localhost:8000/admin/

## 🎮 Features

- **🏎️ Mario Kart Theme**: Racing-inspired UI with emojis and styling
- **📱 QR Code Scanning**: Direct camera access for scanning VDV tickets
- **🔍 Smart Name Extraction**: Improved BeautifulSoup-based HTML parsing
- **⚙️ Product Management**: Add and manage racing "power-ups"
- **🌟 Mobile-First Design**: Optimized for smartphone use

## 🔧 Development Features

### Key Improvements Made:
- ✅ **Fixed passenger name extraction** - No more false positives like "English" or "title"
- ✅ **BeautifulSoup parsing** - Robust HTML parsing instead of regex
- ✅ **Multiple extraction strategies** - Table cells, headers, bold text
- ✅ **Smart filtering** - Ignores non-name content automatically

### Technical Stack:
- **Backend**: Django 5.0
- **Frontend**: HTML5, CSS3, JavaScript (Mario Kart themed)
- **QR Scanner**: Barkoder SDK
- **Ticket Processing**: Integration with zuegli.app API
- **HTML Parsing**: BeautifulSoup4
- **Database**: SQLite (development)

## 🛠️ Development Commands

```bash
# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild after changes
docker-compose up --build

# Run Django commands
docker-compose exec ftqoin-scanner python manage.py <command>

# Access container shell
docker-compose exec ftqoin-scanner bash
```

## 🎯 How It Works

1. **QR Scanning**: Uses device camera to scan VDV train tickets
2. **API Processing**: Sends ticket data to zuegli.app for validation
3. **Name Extraction**: Uses BeautifulSoup to parse HTML and extract passenger names
4. **Product Selection**: Users can select racing "power-ups" after scanning
5. **Order Processing**: Generates API-ready order data

## 🏆 Testing the Passenger Name Fix

The main improvement is the passenger name extraction. The system now:

- ✅ Correctly identifies table cells containing passenger information
- ✅ Filters out non-name content like "title", "English", "German"
- ✅ Handles different name formats (First Last, LAST FIRST, etc.)
- ✅ Uses multiple fallback strategies for robust extraction

## 📱 Mobile Usage

For the best experience:
1. Open http://localhost:8000/ on your smartphone
2. Allow camera permissions when prompted
3. Point camera at a VDV QR code to scan
4. Watch for "User Identified" message with extracted name
5. Select power-ups and submit your racing order!

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Stop any existing containers
docker-compose down

# Or use a different port
docker run -p 8001:8000 ftqoin-scanner
```

### Camera Not Working
- Ensure HTTPS or localhost (camera requires secure context)
- Check browser permissions for camera access
- Try a different browser if issues persist

### Static Files Not Loading
```bash
# Rebuild with fresh static files
docker-compose down
docker-compose up --build
```

## 🚧 Known Limitations

- Camera access requires HTTPS or localhost
- VDV ticket processing depends on zuegli.app API availability
- Some ticket formats may not contain passenger names

## 🎉 Success Criteria

You'll know it's working when:
- ✅ Mario Kart themed interface loads
- ✅ Camera scanner initializes ("Race Scanner Ready!")
- ✅ QR codes can be scanned successfully
- ✅ Passenger names are extracted correctly (not "English" or "title")
- ✅ Settings page allows product management

---

**🏁 Happy Racing! 🏎️**