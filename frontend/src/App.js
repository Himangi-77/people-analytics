import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';
import { Send, Upload, Users, Network, BarChart3, MessageSquare, Palette, Maximize2, Layout } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Textarea } from './components/ui/textarea';
import { Badge } from './components/ui/badge';
import { Alert, AlertDescription } from './components/ui/alert';
import { Separator } from './components/ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import './App.css';

// Register cytoscape extensions
cytoscape.use(coseBilkent);

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Home() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [graphStats, setGraphStats] = useState(null);
  const [graphUploaded, setGraphUploaded] = useState(false);
  const [error, setError] = useState('');
  const [nodeSizeBy, setNodeSizeBy] = useState('degree');
  const [nodeColorBy, setNodeColorBy] = useState('department');
  const [graphLayout, setGraphLayout] = useState('cose-bilkent');
  
  const cyRef = useRef(null);
  const graphContainerRef = useRef(null);

  // Sample questions
  const sampleQuestions = [
    "Who are the informal leaders in our organization, and how do they influence decision-making?",
    "Which teams are most at risk of becoming silos, and what connections should we strengthen?",
    "Where are the communication bottlenecks that could slow down strategy execution?",
    "How effectively is knowledge flowing between departments like Sales, Engineering, and Marketing?",
    "Who are the most central connectors in hybrid work settings, and are they distributed evenly or concentrated?"
  ];

  // Node sizing options
  const sizingOptions = [
    { value: 'degree', label: 'Degree (Connections)' },
    { value: 'betweenness', label: 'Betweenness Centrality' },
    { value: 'gate_keeper_score', label: 'Gatekeeper Score' },
    { value: 'go_to_score', label: 'Go-To Score' },
    { value: 'social_hubs_score', label: 'Social Hubs Score' },
    { value: 'tenure_year', label: 'Tenure (Years)' },
    { value: 'rating', label: 'Performance Rating' },
    { value: 'hierarchy_level', label: 'Hierarchy Level' }
  ];

  // Node coloring options
  const coloringOptions = [
    { value: 'department', label: 'Department' },
    { value: 'gender', label: 'Gender' },
    { value: 'hierarchy_level', label: 'Hierarchy Level' },
    { value: 'tenure_status', label: 'Tenure Status' },
    { value: 'group_name1', label: 'Group 1' },
    { value: 'group_name2', label: 'Group 2' },
    { value: 'location', label: 'Location' },
    { value: 'rating', label: 'Performance Rating' }
  ];

  // Initialize with sample data
  useEffect(() => {
    createSampleGraph();
    loadGraphStats();
  }, []);

  const createSampleGraph = async () => {
    // Create sample organizational data  
    const sampleGraphData = {
      nodes: [
        { data: { id: '1', name: 'Alice Johnson', department: 'Engineering', title: 'Tech Lead', group: 'backend' } },
        { data: { id: '2', name: 'Bob Chen', department: 'Engineering', title: 'Senior Developer', group: 'frontend' } },
        { data: { id: '3', name: 'Carol Davis', department: 'Marketing', title: 'Marketing Manager', group: 'content' } },
        { data: { id: '4', name: 'David Wilson', department: 'Sales', title: 'Sales Director', group: 'enterprise' } },
        { data: { id: '5', name: 'Emily Brown', department: 'Engineering', title: 'DevOps Engineer', group: 'infrastructure' } },
        { data: { id: '6', name: 'Frank Miller', department: 'Marketing', title: 'Content Specialist', group: 'content' } },
        { data: { id: '7', name: 'Grace Lee', department: 'Sales', title: 'Account Executive', group: 'mid-market' } },
        { data: { id: '8', name: 'Henry Garcia', department: 'Engineering', title: 'Product Manager', group: 'product' } },
        { data: { id: '9', name: 'Iris Thompson', department: 'Marketing', title: 'Designer', group: 'creative' } },
        { data: { id: '10', name: 'Jack Rodriguez', department: 'Sales', title: 'Sales Rep', group: 'smb' } },
        { data: { id: '11', name: 'Karen White', department: 'HR', title: 'HR Director', group: 'people' } },
        { data: { id: '12', name: 'Luke Anderson', department: 'Engineering', title: 'Data Scientist', group: 'analytics' } },
        { data: { id: '13', name: 'Maria Lopez', department: 'Marketing', title: 'Social Media Manager', group: 'social' } },
        { data: { id: '14', name: 'Nathan Clark', department: 'Sales', title: 'Customer Success', group: 'support' } },
        { data: { id: '15', name: 'Olivia Taylor', department: 'Engineering', title: 'Security Engineer', group: 'security' } }
      ],
      edges: [
        { data: { id: 'e1', source: '1', target: '2', weight: 0.8, type: 'collaboration' } },
        { data: { id: 'e2', source: '1', target: '5', weight: 0.6, type: 'technical' } },
        { data: { id: 'e3', source: '1', target: '8', weight: 0.9, type: 'project' } },
        { data: { id: 'e4', source: '2', target: '3', weight: 0.4, type: 'cross-team' } },
        { data: { id: 'e5', source: '3', target: '4', weight: 0.7, type: 'go-to-market' } },
        { data: { id: 'e6', source: '3', target: '6', weight: 0.8, type: 'collaboration' } },
        { data: { id: 'e7', source: '4', target: '7', weight: 0.9, type: 'mentoring' } },
        { data: { id: 'e8', source: '4', target: '10', weight: 0.6, type: 'supervision' } },
        { data: { id: 'e9', source: '5', target: '12', weight: 0.5, type: 'infrastructure' } },
        { data: { id: 'e10', source: '6', target: '9', weight: 0.7, type: 'creative' } },
        { data: { id: 'e11', source: '7', target: '14', weight: 0.8, type: 'customer' } },
        { data: { id: 'e12', source: '8', target: '12', weight: 0.6, type: 'data' } },
        { data: { id: 'e13', source: '9', target: '13', weight: 0.5, type: 'marketing' } },
        { data: { id: 'e14', source: '11', target: '1', weight: 0.4, type: 'hr-support' } },
        { data: { id: 'e15', source: '11', target: '4', weight: 0.5, type: 'hr-support' } },
        { data: { id: 'e16', source: '11', target: '3', weight: 0.3, type: 'hr-support' } },
        { data: { id: 'e17', source: '8', target: '3', weight: 0.6, type: 'product-marketing' } },
        { data: { id: 'e18', source: '15', target: '1', weight: 0.5, type: 'security' } },
        { data: { id: 'e19', source: '15', target: '5', weight: 0.7, type: 'security' } }
      ]
    };

    try {
      console.log('Uploading sample graph data...');
      
      const response = await fetch(`${API}/upload-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ graph_data: sampleGraphData })
      });

      const result = await response.json();
      console.log('Upload response:', result);

      if (response.ok) {
        setGraphUploaded(true);
        setError('');
        
        // Initialize visualization with a delay to ensure container is ready
        setTimeout(() => {
          if (graphContainerRef.current) {
            initializeGraph(sampleGraphData);
          }
        }, 500);
      } else {
        setError(`Failed to upload graph: ${result.detail || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Failed to upload sample graph:', err);
      setError('Failed to initialize sample data');
    }
  };

  const loadGraphStats = async () => {
    try {
      const response = await fetch(`${API}/graph-stats`);
      if (response.ok) {
        const stats = await response.json();
        setGraphStats(stats);
      }
    } catch (err) {
      console.error('Failed to load graph stats:', err);
    }
  };

  const getNodeColor = (node, colorBy) => {
    const data = node.data();
    
    switch (colorBy) {
      case 'department':
        const deptColors = {
          'HDFC': '#3B82F6',
          'Engineering': '#10B981',
          'Marketing': '#EF4444',
          'Sales': '#F59E0B',
          'HR': '#8B5CF6',
          'Finance': '#EC4899'
        };
        return deptColors[data.department] || '#6B7280';
      
      case 'gender':
        return data.gender === 'Male' ? '#3B82F6' : data.gender === 'Female' ? '#EC4899' : '#6B7280';
      
      case 'hierarchy_level':
        const level = data.hierarchy_level || 5;
        const levelColors = ['#DC2626', '#EA580C', '#D97706', '#CA8A04', '#65A30D', '#16A34A', '#059669', '#0891B2'];
        return levelColors[Math.min(level - 1, 7)] || '#6B7280';
      
      case 'tenure_status':
        const statusColors = {
          'new hire': '#EF4444',
          'tenured': '#10B981',
          'senior': '#3B82F6'
        };
        return statusColors[data.tenure_status] || '#6B7280';
      
      case 'rating':
        const rating = data.rating || 5;
        if (rating >= 9) return '#10B981';
        if (rating >= 7) return '#F59E0B';
        if (rating >= 5) return '#EF4444';
        return '#6B7280';
      
      default:
        return '#6B7280';
    }
  };

  const getNodeSize = (node, sizeBy) => {
    const data = node.data();
    let value = 0;
    
    switch (sizeBy) {
      case 'degree':
        value = data.degree || 0;
        return Math.max(20, Math.min(80, value * 3 + 20));
      
      case 'betweenness':
        value = data.betweenness || 0;
        return Math.max(20, Math.min(80, value * 1000 + 20));
      
      case 'gate_keeper_score':
        value = data.gate_keeper_score || 0;
        return Math.max(20, Math.min(80, value * 500 + 20));
      
      case 'go_to_score':
        value = data.go_to_score || 0;
        return Math.max(20, Math.min(80, value * 200 + 20));
      
      case 'social_hubs_score':
        value = data.social_hubs_score || 0;
        return Math.max(20, Math.min(80, value * 200 + 20));
      
      case 'tenure_year':
        value = data.tenure_year || 0;
        return Math.max(20, Math.min(80, value * 2 + 20));
      
      case 'rating':
        value = data.rating || 5;
        return Math.max(20, Math.min(80, value * 6 + 20));
      
      case 'hierarchy_level':
        value = 8 - (data.hierarchy_level || 5); // Invert so higher levels are bigger
        return Math.max(20, Math.min(80, value * 8 + 20));
      
      default:
        return 30;
    }
  };

  const initializeGraph = (graphData) => {
    if (!graphContainerRef.current) return;

    console.log('Initializing graph with data:', graphData);

    // Clear existing graph
    if (cyRef.current) {
      cyRef.current.destroy();
    }

    // Prepare elements for Cytoscape
    const elements = [
      ...graphData.nodes,
      ...graphData.edges
    ];

    console.log('Elements for Cytoscape:', elements);

    // Create new cytoscape instance
    cyRef.current = cytoscape({
      container: graphContainerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (node) => getNodeColor(node, nodeColorBy),
            'label': (node) => {
              const name = node.data('name') || node.data('full_name') || node.data('id');
              return typeof name === 'string' ? name : String(name);
            },
            'width': (node) => getNodeSize(node, nodeSizeBy),
            'height': (node) => getNodeSize(node, nodeSizeBy),
            'font-size': '10px',
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#ffffff',
            'text-outline-color': '#000000',
            'text-outline-width': 1,
            'border-width': 2,
            'border-color': '#ffffff',
            'text-wrap': 'ellipsis',
            'text-max-width': '60px'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': (edge) => (edge.data('weight') || 0.5) * 4,
            'line-color': '#94A3B8',
            'target-arrow-color': '#94A3B8',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'opacity': 0.7
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-color': '#FCD34D',
            'border-width': 4
          }
        }
      ],
      layout: {
        name: 'cose-bilkent',
        animate: true,
        animationDuration: 1000,
        nodeRepulsion: 8000,
        idealEdgeLength: 100,
        edgeElasticity: 0.1
      }
    });

    // Add interactivity
    cyRef.current.on('tap', 'node', (evt) => {
      const node = evt.target;
      console.log('Selected node:', node.data());
    });
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });

      if (response.ok) {
        const result = await response.json();
        setResponse(result);
        
        // Update graph visualization with subgraph
        if (cyRef.current && result.subgraph) {
          cyRef.current.elements().remove();
          cyRef.current.add(result.subgraph.nodes);
          cyRef.current.add(result.subgraph.edges);
          
          // Re-run layout
          cyRef.current.layout({
            name: 'cose-bilkent',
            animate: true,
            animationDuration: 1000
          }).run();
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to process query');
      }
    } catch (err) {
      console.error('Query failed:', err);
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuestion = (sampleQ) => {
    setQuestion(sampleQ);
  };

  const updateGraphVisualization = () => {
    if (cyRef.current) {
      cyRef.current.style().selector('node').style({
        'background-color': (node) => getNodeColor(node, nodeColorBy),
        'width': (node) => getNodeSize(node, nodeSizeBy),
        'height': (node) => getNodeSize(node, nodeSizeBy)
      }).update();
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    console.log('File selected:', file.name, file.type, file.size);
    setError(''); // Clear any previous errors
    setLoading(true); // Show loading state

    try {
      // Read the file content
      const text = await file.text();
      console.log('File content read, length:', text.length);
      
      // Parse JSON
      const rawData = JSON.parse(text);
      console.log('JSON parsed successfully:', rawData);
      
      // Handle different graph formats
      let graphData;
      
      // Check if it's the nested format: {graph: {elements: {nodes: [], edges: []}}}
      if (rawData.graph && rawData.graph.elements && rawData.graph.elements.nodes && rawData.graph.elements.edges) {
        console.log('Detected nested graph format (main_combined.json style)');
        graphData = rawData.graph.elements;
      }
      // Check if it's the simple format: {nodes: [], edges: []}
      else if (rawData.nodes && rawData.edges) {
        console.log('Detected simple graph format');
        graphData = rawData;
      }
      // Check if it's already in elements format: {nodes: [], edges: []}
      else if (rawData.elements && rawData.elements.nodes && rawData.elements.edges) {
        console.log('Detected elements format');
        graphData = rawData.elements;
      }
      else {
        throw new Error('Invalid graph format. Expected JSON with one of these structures:\n1. {nodes: [], edges: []}\n2. {graph: {elements: {nodes: [], edges: []}}}\n3. {elements: {nodes: [], edges: []}}');
      }
      
      console.log(`Graph contains ${graphData.nodes.length} nodes and ${graphData.edges.length} edges`);
      
      // Upload to backend
      const response = await fetch(`${API}/upload-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ graph_data: graphData })
      });

      const result = await response.json();
      console.log('Upload response:', result);

      if (response.ok) {
        setGraphUploaded(true);
        setError('');
        
        // Show success message
        console.log(`Graph uploaded successfully! ${result.stats.nodes} nodes, ${result.stats.edges} edges`);
        
        // Initialize visualization
        initializeGraph(graphData);
        loadGraphStats();
      } else {
        setError(`Upload failed: ${result.detail || 'Unknown error'}`);
        console.error('Upload failed:', result);
      }
    } catch (err) {
      console.error('File upload error:', err);
      if (err.name === 'SyntaxError') {
        setError('Invalid JSON file format. Please check your file structure.');
      } else {
        setError(`Upload error: ${err.message}`);
      }
    } finally {
      setLoading(false);
      // Reset the file input so the same file can be uploaded again
      e.target.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Network className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">People Analytics</h1>
            </div>
            <div className="flex items-center space-x-4">
              {graphStats && (
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <div className="flex items-center space-x-1">
                    <Users className="h-4 w-4" />
                    <span>{graphStats.nodes} People</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <BarChart3 className="h-4 w-4" />
                    <span>{graphStats.edges} Connections</span>
                  </div>
                </div>
              )}
              <input
                type="file"
                accept=".json"
                onChange={handleFileUpload}
                className="sr-only"
                id="file-upload"
                disabled={loading}
              />
              <label
                htmlFor="file-upload"
                className={`inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500 cursor-pointer transition-colors ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-gray-400 border-t-gray-700 rounded-full animate-spin" />
                    <span>Uploading...</span>
                  </div>
                ) : (
                  <>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Graph
                  </>
                )}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Query Panel */}
          <div className="lg:col-span-1 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MessageSquare className="h-5 w-5" />
                  <span>Ask a Question</span>
                </CardTitle>
                <CardDescription>
                  Ask natural language questions about your organizational network
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <form onSubmit={handleQuery} className="space-y-4">
                  <Textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="e.g., Who are the key influencers in our organization?"
                    rows={4}
                    className="resize-none"
                  />
                  <Button 
                    type="submit" 
                    disabled={loading || !question.trim()}
                    className="w-full"
                  >
                    {loading ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span>Analyzing...</span>
                      </div>
                    ) : (
                      <>
                        <Send className="h-4 w-4 mr-2" />
                        Ask Question
                      </>
                    )}
                  </Button>
                </form>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-3">Sample Questions:</h3>
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {sampleQuestions.slice(0, 3).map((q, idx) => (
                      <Button
                        key={idx}
                        variant="ghost"
                        size="sm"
                        onClick={() => handleSampleQuestion(q)}
                        className="w-full text-left justify-start h-auto p-2 text-xs leading-tight break-words whitespace-normal"
                      >
                        <span className="line-clamp-3">{q}</span>
                      </Button>
                    ))}
                  </div>
                </div>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Graph Upload Format:</h3>
                  <div className="text-xs text-gray-600 space-y-1">
                    <p>Upload a JSON file with this structure:</p>
                    <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`{
  "nodes": [
    {
      "data": {
        "id": "person_1",
        "name": "John Doe",
        "department": "Engineering",
        "title": "Developer"
      }
    }
  ],
  "edges": [
    {
      "data": {
        "id": "edge_1",
        "source": "person_1",
        "target": "person_2",
        "weight": 0.8,
        "type": "collaboration"
      }
    }
  ]
}`}
                    </pre>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Graph Controls */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Palette className="h-5 w-5" />
                  <span>Graph Controls</span>
                </CardTitle>
                <CardDescription>
                  Customize node appearance based on organizational metrics
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    <Maximize2 className="h-4 w-4 inline mr-1" />
                    Size Nodes By:
                  </label>
                  <Select value={nodeSizeBy} onValueChange={(value) => {
                    setNodeSizeBy(value);
                    // Re-render graph with new sizing
                    if (cyRef.current) {
                      cyRef.current.style().selector('node').style({
                        'width': (node) => getNodeSize(node, value),
                        'height': (node) => getNodeSize(node, value)
                      }).update();
                    }
                  }}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {sizingOptions.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    <Palette className="h-4 w-4 inline mr-1" />
                    Color Nodes By:
                  </label>
                  <Select value={nodeColorBy} onValueChange={(value) => {
                    setNodeColorBy(value);
                    // Re-render graph with new coloring
                    if (cyRef.current) {
                      cyRef.current.style().selector('node').style({
                        'background-color': (node) => getNodeColor(node, value)
                      }).update();
                    }
                  }}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {coloringOptions.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Legend */}
                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <h4 className="text-xs font-semibold text-gray-700 mb-2">Legend:</h4>
                  <div className="space-y-1 text-xs text-gray-600">
                    <div>• Node size reflects {sizingOptions.find(o => o.value === nodeSizeBy)?.label}</div>
                    <div>• Node color reflects {coloringOptions.find(o => o.value === nodeColorBy)?.label}</div>
                    <div>• Click nodes for details</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Results Panel */}
            {response && (
              <Card>
                <CardHeader>
                  <CardTitle>Analysis Results</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">AI Insights:</h4>
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {response.answer}
                    </p>
                  </div>
                  
                  <Separator />
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Key Metrics:</h4>
                    <div className="space-y-1">
                      {response.insights.map((insight, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {insight}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Graph Visualization */}
          <div className="lg:col-span-2">
            <Card className="h-full">
              <CardHeader>
                <CardTitle>Network Visualization</CardTitle>
                <CardDescription>
                  Interactive organizational network graph
                </CardDescription>
              </CardHeader>
              <CardContent>
                {error && (
                  <Alert className="mb-4">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                <div 
                  ref={graphContainerRef}
                  className="w-full h-96 lg:h-[600px] border rounded-lg bg-gray-50"
                  style={{ minHeight: '400px' }}
                />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;