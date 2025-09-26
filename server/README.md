# Server Setup with Python CLIP Integration

This server provides a Node.js API with Python CLIP (Contrastive Language-Image Pre-training) integration for image comparison.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Installation

1. **Clone and navigate to server directory:**
   ```bash
   cd server
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Set up Python environment:**
   
   **Windows:**
   ```bash
   # Option 1: Run setup script
   setup-python.bat
   
   # Option 2: Manual setup
   npm run python:setup
   ```
   
   **Linux/macOS:**
   ```bash
   # Option 1: Run setup script
   chmod +x setup-python.sh
   ./setup-python.sh
   
   # Option 2: Manual setup
   npm run python:setup
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

## 🐍 Python Environment Management

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run python:setup` | Complete Python environment setup |
| `npm run python:create-env` | Create virtual environment only |
| `npm run python:install` | Install Python dependencies |
| `npm run python:test` | Test CLIP API connection |
| `npm run python:clean` | Remove Python environment |
| `npm run setup` | Full setup (Node.js + Python) |

### Manual Python Environment

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv python-env

# Activate environment
# Windows:
python-env\Scripts\activate
# Linux/macOS:
source python-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

```
server/
├── python-scripts/          # Python CLIP scripts
│   ├── clip_compare_flexible.py   # Main comparison script
│   └── test_clip_api.py           # API test client
├── python-env/              # Python virtual environment (gitignored)
├── src/                     # Node.js source code
│   ├── controllers/
│   │   └── clip.controller.ts     # CLIP API controller
│   └── routes/
│       └── api/
│           └── clip.route.ts      # CLIP API routes
├── uploads/                 # Temporary file uploads (gitignored)
├── requirements.txt         # Python dependencies
├── setup-python.bat        # Windows Python setup
├── setup-python.sh         # Linux/macOS Python setup
└── package.json            # Node.js dependencies and scripts
```

## 🔗 API Endpoints

### CLIP Image Comparison

**POST** `/api/clip/compare`
- Compare two images with optional text tag
- **Body:** `multipart/form-data`
  - `image1`: Image file (required)
  - `image2`: Image file (required) 
  - `tag`: Text description (optional)

**GET** `/api/clip/info`
- Get API information and usage details

### Example Usage

```bash
# Test API info
npm run python:test -- --info

# Compare two images
npm run python:test -- --image1 path/to/image1.jpg --image2 path/to/image2.jpg

# Compare with text tag
npm run python:test -- --image1 path/to/image1.jpg --image2 path/to/image2.jpg --tag "a red car"
```

## 🛠️ Development

### Environment Variables

Create a `.env` file in the server directory:

```env
PORT=5003
NODE_ENV=development
```

### Testing Python Integration

```bash
# Test Python environment
python-env/Scripts/python python-scripts/test_clip_api.py --info

# Test with sample images (replace with actual paths)
python-env/Scripts/python python-scripts/test_clip_api.py --image1 test1.jpg --image2 test2.jpg
```

## 📦 Dependencies

### Node.js Dependencies
- Express.js for API server
- Multer for file uploads
- TypeScript for type safety

### Python Dependencies
- PyTorch for deep learning
- CLIP for image-text understanding
- Pillow for image processing
- Requests for HTTP testing

## 🚨 Before Git Commit

The `.gitignore` is configured to exclude:
- ✅ `python-env/` - Virtual environment
- ✅ `uploads/*` - Temporary uploads
- ✅ `__pycache__/` - Python cache files
- ✅ `*.pyc` - Compiled Python files
- ✅ `.env` - Environment variables

### Pre-commit Checklist
- [ ] Python environment is working: `npm run python:test`
- [ ] Node.js server starts: `npm run dev`
- [ ] No sensitive files in git: `git status`
- [ ] All tests pass

## 🐛 Troubleshooting

### Python Issues
1. **"Python not found"**: Install Python 3.8+ and add to PATH
2. **"pip install failed"**: Try upgrading pip: `python -m pip install --upgrade pip`
3. **CUDA/GPU issues**: Install appropriate PyTorch version from [pytorch.org](https://pytorch.org)

### Node.js Issues
1. **"Port already in use"**: Change PORT in `.env` or kill existing process
2. **"Module not found"**: Run `npm install`

### Integration Issues
1. **"Python script error"**: Check python-env activation in controller
2. **"File upload failed"**: Ensure uploads/ directory exists

## 📚 Additional Resources

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [PyTorch Installation](https://pytorch.org/get-started/locally/)
- [Express.js Documentation](https://expressjs.com/)