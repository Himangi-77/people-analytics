import React, { useState } from 'react';
import { Upload } from 'lucide-react';

function TestUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setUploadStatus(file ? `Selected: ${file.name}` : 'No file selected');
    console.log('File selected:', file);
  };

  const triggerFileInput = () => {
    document.getElementById('test-file-input').click();
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>Upload Test Page</h2>
      
      {/* Method 1: Hidden input with label */}
      <div style={{ marginBottom: '20px' }}>
        <h3>Method 1: Label + Hidden Input</h3>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="hidden-file-input"
        />
        <label 
          htmlFor="hidden-file-input"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            padding: '8px 16px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
            backgroundColor: '#f9f9f9'
          }}
        >
          <Upload style={{ width: '16px', height: '16px', marginRight: '8px' }} />
          Upload Graph (Method 1)
        </label>
      </div>

      {/* Method 2: Button that triggers input click */}
      <div style={{ marginBottom: '20px' }}>
        <h3>Method 2: Button + Hidden Input</h3>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="test-file-input"
        />
        <button 
          onClick={triggerFileInput}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            padding: '8px 16px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
            backgroundColor: '#f0f0f0'
          }}
        >
          <Upload style={{ width: '16px', height: '16px', marginRight: '8px' }} />
          Upload Graph (Method 2)
        </button>
      </div>

      {/* Method 3: Direct file input */}
      <div style={{ marginBottom: '20px' }}>
        <h3>Method 3: Direct Input</h3>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
        />
      </div>

      {/* Status display */}
      {uploadStatus && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: selectedFile ? '#d4edda' : '#f8d7da',
          border: '1px solid ' + (selectedFile ? '#c3e6cb' : '#f5c6cb'),
          borderRadius: '4px',
          marginTop: '20px'
        }}>
          Status: {uploadStatus}
        </div>
      )}
    </div>
  );
}

export default TestUpload;