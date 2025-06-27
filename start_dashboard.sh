#!/bin/bash
echo "🚀 Starting Snowflake Analytics Dashboard..."
echo "📊 Opening on http://localhost:8509"
echo "🔥 Press Ctrl+C to stop the server"
echo ""
python3 -m streamlit run app.py --server.port 8509
