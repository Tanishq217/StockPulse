import React, { useState, useEffect, useMemo } from 'react';

const CATEGORIES = [
  'All Categories',
  'Electronics',
  'Electrical',
  'Hardware',
  'Robotics',
  'Machinery',
  'Tools',
  'Raw Materials',
];

const CATEGORY_COLORS = {
  Electronics: '#3b82f6',
  Electrical: '#06b6d4',
  Hardware: '#8b5cf6',
  Robotics: '#ec4899',
  Machinery: '#f59e0b',
  Tools: '#10b981',
  'Raw Materials': '#64748b',
};

export default function App() {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({
    total_skus: 0,
    total_units: 0,
    total_valuation: 0,
    low_stock_count: 0,
    out_of_stock_count: 0,
    in_stock_count: 0,
    categories: {},
  });
  const [health, setHealth] = useState({ status: 'checking', version: '-', latency: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('inventory'); // 'inventory' | 'architecture' | 'metrics'

  // Filters
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [statusFilter, setStatusFilter] = useState('ALL');

  // Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({
    sku: '',
    name: '',
    category: 'Electronics',
    quantity: 15,
    min_threshold: 10,
    unit_price: 25.0,
    supplier: '',
    location: '',
  });

  // Toast Notification
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  const fetchData = async () => {
    const startTime = performance.now();
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (search) params.append('q', search);
      if (selectedCategory !== 'All Categories') params.append('category', selectedCategory);
      if (statusFilter !== 'ALL') params.append('stock_status', statusFilter.toLowerCase());

      const [itemsRes, statsRes, healthRes] = await Promise.all([
        fetch(`/api/inventory?${params.toString()}`),
        fetch('/api/inventory/stats'),
        fetch('/health'),
      ]);

      const latencyMs = Math.round(performance.now() - startTime);

      if (!itemsRes.ok) throw new Error(`API Error: ${itemsRes.status}`);

      const itemsData = await itemsRes.json();
      const statsData = statsRes.ok ? await statsRes.json() : stats;
      const healthData = healthRes.ok ? await healthRes.json() : { status: 'offline' };

      setItems(itemsData);
      setStats(statsData);
      setHealth({ ...healthData, latency: latencyMs });
    } catch (err) {
      console.error('Fetch error:', err);
      setError('Unable to reach StockPulse Backend. Ensure backend service is running on port 8000.');
      setHealth({ status: 'offline', version: '-', latency: null });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [search, selectedCategory, statusFilter]);

  const generateRandomSku = () => {
    const prefix = formData.category.slice(0, 3).toUpperCase();
    const rand = Math.floor(1000 + Math.random() * 9000);
    return `${prefix}-${rand}`;
  };

  const handleOpenCreateModal = () => {
    setEditingItem(null);
    setFormData({
      sku: `ELE-${Math.floor(1000 + Math.random() * 9000)}`,
      name: '',
      category: 'Electronics',
      quantity: 25,
      min_threshold: 10,
      unit_price: 49.99,
      supplier: 'Sensirion Tech Corp',
      location: 'Warehouse A - Bay 3',
    });
    setModalOpen(true);
  };

  const handleOpenEditModal = (item) => {
    setEditingItem(item);
    setFormData({
      sku: item.sku,
      name: item.name,
      category: item.category,
      quantity: item.quantity,
      min_threshold: item.min_threshold,
      unit_price: item.unit_price,
      supplier: item.supplier || '',
      location: item.location || '',
    });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = editingItem
        ? `/api/inventory/${editingItem.id}`
        : '/api/inventory';
      const method = editingItem ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          quantity: parseInt(formData.quantity, 10),
          min_threshold: parseInt(formData.min_threshold, 10),
          unit_price: parseFloat(formData.unit_price),
        }),
      });

      if (!res.ok) {
        const errorDetail = await res.json();
        throw new Error(errorDetail.detail || 'Failed to save item');
      }

      setModalOpen(false);
      showToast(editingItem ? `Updated "${formData.name}" successfully` : `Created "${formData.name}" successfully`);
      fetchData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleQuickRestock = async (item, delta = 10) => {
    try {
      const newQty = item.quantity + delta;
      const res = await fetch(`/api/inventory/${item.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quantity: newQty,
        }),
      });

      if (!res.ok) throw new Error('Failed to restock item');
      showToast(`Restocked ${item.name} (+${delta} units)`, 'success');
      fetchData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete "${name}" from inventory?`)) return;
    try {
      const res = await fetch(`/api/inventory/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete item');
      showToast(`Deleted "${name}"`, 'success');
      fetchData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Category distribution calculation
  const categoryStats = useMemo(() => {
    if (!stats.categories || Object.keys(stats.categories).length === 0) return [];
    const total = Object.values(stats.categories).reduce((acc, c) => acc + c.count, 0) || 1;
    return Object.entries(stats.categories).map(([name, data]) => ({
      name,
      count: data.count,
      valuation: data.valuation,
      percentage: Math.round((data.count / total) * 100),
      color: CATEGORY_COLORS[name] || '#94a3b8',
    })).sort((a, b) => b.count - a.count);
  }, [stats]);

  return (
    <div className="app-layout">
      {/* Toast Notification */}
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          <span className="toast-icon">{toast.type === 'success' ? '✓' : '⚠️'}</span>
          <span>{toast.message}</span>
        </div>
      )}

      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon-wrapper">
            <div className="brand-pulse-ring" />
            <span className="brand-icon">⚡</span>
          </div>
          <div>
            <span className="brand-name">StockPulse</span>
            <span className="brand-badge">CLOUD NATIVE</span>
          </div>
        </div>

        <div className="nav-section-title">MANAGEMENT</div>
        <ul className="nav-links">
          <li
            className={`nav-item ${activeTab === 'inventory' ? 'active' : ''}`}
            onClick={() => setActiveTab('inventory')}
          >
            <span className="nav-icon">📦</span>
            <span>Inventory Catalog</span>
            <span className="nav-count">{stats.total_skus}</span>
          </li>
          <li
            className={`nav-item ${activeTab === 'architecture' ? 'active' : ''}`}
            onClick={() => setActiveTab('architecture')}
          >
            <span className="nav-icon">🏛️</span>
            <span>3-Tier Architecture</span>
          </li>
          <li
            className={`nav-item ${activeTab === 'metrics' ? 'active' : ''}`}
            onClick={() => setActiveTab('metrics')}
          >
            <span className="nav-icon">📊</span>
            <span>DevOps Probes</span>
          </li>
        </ul>

        <div className="nav-section-title" style={{ marginTop: '1.5rem' }}>QUICK ENDPOINTS</div>
        <ul className="nav-links">
          <li>
            <a href="/docs" target="_blank" rel="noreferrer" className="nav-item external-link">
              <span className="nav-icon">📄</span>
              <span>FastAPI Swagger UI</span>
              <span className="nav-arrow">↗</span>
            </a>
          </li>
          <li>
            <a href="/health" target="_blank" rel="noreferrer" className="nav-item external-link">
              <span className="nav-icon">🩺</span>
              <span>Health Liveness API</span>
              <span className="nav-arrow">↗</span>
            </a>
          </li>
          <li>
            <a href="/metrics" target="_blank" rel="noreferrer" className="nav-item external-link">
              <span className="nav-icon">📈</span>
              <span>Prometheus Stream</span>
              <span className="nav-arrow">↗</span>
            </a>
          </li>
        </ul>

        {/* Live System Status Pill Box */}
        <div className="system-status-box">
          <div className="status-header">
            <span
              className="status-pulse-dot"
              style={{
                backgroundColor: health.status === 'up' ? '#10b981' : '#ef4444',
                boxShadow: health.status === 'up' ? '0 0 12px #10b981' : '0 0 12px #ef4444',
              }}
            />
            <span className="status-text">
              BACKEND: {health.status.toUpperCase()}
            </span>
            {health.latency !== null && (
              <span className="status-ping">{health.latency}ms</span>
            )}
          </div>
          <div className="status-meta">
            <div>Engine: FastAPI v{health.version || '1.0.0'}</div>
            <div>Runtime: Docker / Kubernetes Kind</div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {/* Top Header Bar */}
        <header className="top-bar">
          <div>
            <div className="breadcrumbs">
              <span>Cloud Cluster</span> / <span>StockPulse Production</span> / <span>Catalog</span>
            </div>
            <h1>Warehouse Inventory Control</h1>
            <p>Real-time synchronized inventory management orchestrated with PostgreSQL & FastAPI</p>
          </div>
          <div className="top-actions">
            <button className="btn btn-secondary" onClick={fetchData} title="Refresh catalog data">
              <span className={`refresh-icon ${loading ? 'spinning' : ''}`}>🔄</span>
              <span>Sync DB</span>
            </button>
            <button className="btn btn-primary" onClick={handleOpenCreateModal}>
              <span>+ Add Item</span>
            </button>
          </div>
        </header>

        {/* Error Notification Banner */}
        {error && (
          <div className="error-banner">
            <span className="error-banner-icon">⚠️</span>
            <div>
              <strong>Backend Disconnected:</strong> {error}
            </div>
          </div>
        )}

        {/* 3-Tier Architecture Flow View */}
        {activeTab === 'architecture' ? (
          <section className="architecture-panel">
            <div className="architecture-header">
              <h2>3-Tier Cloud-Native Architecture Map</h2>
              <p>Live request flow and persistence topology across microservices</p>
            </div>
            <div className="tier-flow-grid">
              <div className="tier-card tier-frontend">
                <div className="tier-badge">TIER 1 • PRESENTATION</div>
                <h3>React 18 + Vite</h3>
                <p>Nginx Alpine reverse proxy serving optimized static bundle.</p>
                <div className="tier-meta">
                  <span>Port: <strong>3000</strong></span>
                  <span>Protocol: <strong>HTTP/1.1</strong></span>
                  <span>Health: <strong style={{ color: '#10b981' }}>Active</strong></span>
                </div>
              </div>
              <div className="tier-connector">
                <div className="connector-arrow">⇄</div>
                <div className="connector-label">REST API</div>
              </div>
              <div className="tier-card tier-backend">
                <div className="tier-badge">TIER 2 • APPLICATION</div>
                <h3>FastAPI (Python 3.12)</h3>
                <p>High-performance asynchronous REST endpoints, SQLAlchemy ORM, Alembic migrations.</p>
                <div className="tier-meta">
                  <span>Port: <strong>8000</strong></span>
                  <span>Probes: <strong>/health, /metrics</strong></span>
                  <span>Status: <strong style={{ color: health.status === 'up' ? '#10b981' : '#ef4444' }}>{health.status.toUpperCase()}</strong></span>
                </div>
              </div>
              <div className="tier-connector">
                <div className="connector-arrow">⇄</div>
                <div className="connector-label">SQL Engine</div>
              </div>
              <div className="tier-card tier-database">
                <div className="tier-badge">TIER 3 • STORAGE</div>
                <h3>PostgreSQL 16</h3>
                <p>ACID relational database with persistent named volume <code>stockpulse-postgres-data</code>.</p>
                <div className="tier-meta">
                  <span>Port: <strong>5432</strong></span>
                  <span>Volume: <strong>Encrypted</strong></span>
                  <span>Tables: <strong>inventory_items</strong></span>
                </div>
              </div>
            </div>
          </section>
        ) : null}

        {/* DevOps Probes View */}
        {activeTab === 'metrics' ? (
          <section className="architecture-panel">
            <div className="architecture-header">
              <h2>DevOps Observability & Health Probes</h2>
              <p>Kubernetes readiness, liveness probes, and Prometheus scraping targets</p>
            </div>
            <div className="probes-grid">
              <div className="probe-box">
                <h4>Liveness Probe (/health)</h4>
                <pre>{JSON.stringify(health, null, 2)}</pre>
                <a href="/health" target="_blank" rel="noreferrer" className="btn btn-secondary" style={{ marginTop: '0.75rem' }}>
                  Open Raw JSON ↗
                </a>
              </div>
              <div className="probe-box">
                <h4>Prometheus Metrics (/metrics)</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                  Exposes application requests, memory, CPU, and database query durations.
                </p>
                <a href="/metrics" target="_blank" rel="noreferrer" className="btn btn-secondary">
                  Open Prometheus Stream ↗
                </a>
              </div>
              <div className="probe-box">
                <h4>Interactive API Swagger Docs (/docs)</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                  OpenAPI 3.1 specification for manual endpoint testing and verification.
                </p>
                <a href="/docs" target="_blank" rel="noreferrer" className="btn btn-primary">
                  Open Swagger UI ↗
                </a>
              </div>
            </div>
          </section>
        ) : null}

        {/* Main Inventory Catalog View */}
        {activeTab === 'inventory' && (
          <>
            {/* Live KPI Metric Cards */}
            <section className="kpi-grid">
              <div className="kpi-card card-purple">
                <div className="kpi-card-inner">
                  <div>
                    <div className="kpi-label">Total Registered SKUs</div>
                    <div className="kpi-value">{stats.total_skus}</div>
                    <div className="kpi-subtext">Active catalog entries in database</div>
                  </div>
                  <div className="kpi-icon-pill icon-purple">📦</div>
                </div>
              </div>

              <div className="kpi-card card-cyan">
                <div className="kpi-card-inner">
                  <div>
                    <div className="kpi-label">Total Units on Hand</div>
                    <div className="kpi-value">{stats.total_units.toLocaleString()}</div>
                    <div className="kpi-subtext">Aggregated across all warehouse bays</div>
                  </div>
                  <div className="kpi-icon-pill icon-cyan">📊</div>
                </div>
              </div>

              <div className="kpi-card card-emerald">
                <div className="kpi-card-inner">
                  <div>
                    <div className="kpi-label">Inventory Valuation</div>
                    <div className="kpi-value">
                      ${stats.total_valuation.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </div>
                    <div className="kpi-subtext">Real-time asset value from DB</div>
                  </div>
                  <div className="kpi-icon-pill icon-emerald">💰</div>
                </div>
              </div>

              <div className="kpi-card card-amber">
                <div className="kpi-card-inner">
                  <div>
                    <div className="kpi-label">Stock Status Alerts</div>
                    <div className="kpi-value" style={{ color: stats.low_stock_count > 0 ? '#f59e0b' : '#10b981' }}>
                      {stats.low_stock_count} <span className="kpi-sub-val">/ {stats.out_of_stock_count} OOS</span>
                    </div>
                    <div className="kpi-subtext">
                      {stats.low_stock_count === 0 ? 'All items above safety threshold' : `${stats.low_stock_count} items below minimum safety buffer`}
                    </div>
                  </div>
                  <div className="kpi-icon-pill icon-amber">⚠️</div>
                </div>
              </div>
            </section>

            {/* Category Stock Distribution Bar */}
            {categoryStats.length > 0 && (
              <section className="category-distribution-card">
                <div className="category-distribution-header">
                  <span className="cat-title">Inventory Category Breakdown</span>
                  <span className="cat-sub">Showing SKU proportions across warehouse zones</span>
                </div>
                <div className="progress-stacked-bar">
                  {categoryStats.map((cat) => (
                    <div
                      key={cat.name}
                      className="progress-stacked-segment"
                      style={{
                        width: `${cat.percentage}%`,
                        backgroundColor: cat.color,
                      }}
                      title={`${cat.name}: ${cat.count} SKUs (${cat.percentage}%) - $${cat.valuation.toFixed(2)}`}
                    />
                  ))}
                </div>
                <div className="category-legend">
                  {categoryStats.map((cat) => (
                    <div key={cat.name} className="legend-item">
                      <span className="legend-dot" style={{ backgroundColor: cat.color }} />
                      <span className="legend-name">{cat.name}</span>
                      <span className="legend-count">{cat.count} ({cat.percentage}%)</span>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Filter and Search Bar */}
            <div className="filter-bar">
              <div className="search-box">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  className="search-input"
                  placeholder="Filter by product name, SKU, or supplier..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                {search && (
                  <button className="clear-search-btn" onClick={() => setSearch('')}>
                    ✕
                  </button>
                )}
              </div>

              <div className="filter-controls">
                <select
                  className="select-input"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                  {CATEGORIES.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>

                <div className="status-pills">
                  {[
                    { id: 'ALL', label: 'All Items', count: stats.total_skus },
                    { id: 'IN_STOCK', label: 'In Stock', count: stats.in_stock_count },
                    { id: 'LOW_STOCK', label: 'Low Stock', count: stats.low_stock_count },
                    { id: 'OUT_OF_STOCK', label: 'Out of Stock', count: stats.out_of_stock_count },
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      className={`status-pill ${statusFilter === tab.id ? 'active' : ''}`}
                      onClick={() => setStatusFilter(tab.id)}
                    >
                      <span>{tab.label}</span>
                      <span className="pill-badge">{tab.count}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Inventory Data Table */}
            <div className="table-card">
              {loading ? (
                <div className="loading-state">
                  <div className="loading-spinner" />
                  <p>Synchronizing catalog with PostgreSQL...</p>
                </div>
              ) : items.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-state-icon">📦</div>
                  <h3>No matching warehouse items</h3>
                  <p>Try modifying your search filter or add a new inventory item below.</p>
                  <button className="btn btn-primary" style={{ marginTop: '1rem' }} onClick={handleOpenCreateModal}>
                    + Add New Inventory Item
                  </button>
                </div>
              ) : (
                <div className="table-responsive">
                  <table>
                    <thead>
                      <tr>
                        <th>SKU Code</th>
                        <th>Product Details</th>
                        <th>Category</th>
                        <th>Stock Level</th>
                        <th>Unit Price</th>
                        <th>Valuation</th>
                        <th>Location</th>
                        <th>Status</th>
                        <th style={{ textAlign: 'right' }}>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {items.map((item) => {
                        const stockRatio = item.min_threshold > 0
                          ? Math.min(100, Math.round((item.quantity / item.min_threshold) * 100))
                          : 100;
                        const gaugeColor =
                          item.quantity === 0
                            ? '#ef4444'
                            : item.quantity <= item.min_threshold
                            ? '#f59e0b'
                            : '#10b981';

                        return (
                          <tr key={item.id}>
                            <td>
                              <span className="sku-tag">{item.sku}</span>
                            </td>
                            <td>
                              <div className="product-name">{item.name}</div>
                              {item.supplier && (
                                <div className="product-supplier">🏢 {item.supplier}</div>
                              )}
                            </td>
                            <td>
                              <span
                                className="category-pill"
                                style={{
                                  backgroundColor: `${CATEGORY_COLORS[item.category] || '#64748b'}20`,
                                  color: CATEGORY_COLORS[item.category] || '#94a3b8',
                                  borderColor: `${CATEGORY_COLORS[item.category] || '#64748b'}40`,
                                }}
                              >
                                {item.category}
                              </span>
                            </td>
                            <td>
                              <div className="stock-level-container">
                                <div className="stock-level-meta">
                                  <span className="stock-qty">{item.quantity}</span>
                                  <span className="stock-min">/ min {item.min_threshold}</span>
                                </div>
                                <div className="stock-progress-track">
                                  <div
                                    className="stock-progress-fill"
                                    style={{
                                      width: `${stockRatio}%`,
                                      backgroundColor: gaugeColor,
                                    }}
                                  />
                                </div>
                              </div>
                            </td>
                            <td>
                              <span className="unit-price">${item.unit_price.toFixed(2)}</span>
                            </td>
                            <td>
                              <span className="total-valuation">
                                ${(item.quantity * item.unit_price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                              </span>
                            </td>
                            <td>
                              <span className="location-tag">
                                📍 {item.location || 'Bay 1 - Unassigned'}
                              </span>
                            </td>
                            <td>
                              <span className={`badge badge-${item.status}`}>
                                <span className="badge-dot" />
                                {item.status.replace('_', ' ')}
                              </span>
                            </td>
                            <td style={{ textAlign: 'right' }}>
                              <div className="action-button-group">
                                <button
                                  className="btn-action btn-action-restock"
                                  title="Quick Restock +10 units"
                                  onClick={() => handleQuickRestock(item, 10)}
                                >
                                  +10
                                </button>
                                <button
                                  className="btn-action btn-action-edit"
                                  title="Edit Item"
                                  onClick={() => handleOpenEditModal(item)}
                                >
                                  ✏️
                                </button>
                                <button
                                  className="btn-action btn-action-delete"
                                  title="Delete Item"
                                  onClick={() => handleDelete(item.id, item.name)}
                                >
                                  🗑️
                                </button>
                              </div>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}
      </main>

      {/* Add / Edit Item Modal */}
      {modalOpen && (
        <div className="modal-overlay" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <h2>{editingItem ? 'Edit Inventory Item' : 'Register New Inventory Item'}</h2>
                <p className="modal-subtitle">
                  {editingItem ? `Updating SKU ${editingItem.sku}` : 'Add a new catalog item directly into PostgreSQL'}
                </p>
              </div>
              <button className="close-btn" onClick={() => setModalOpen(false)}>
                &times;
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <div className="label-with-action">
                    <label>SKU Code</label>
                    {!editingItem && (
                      <button
                        type="button"
                        className="btn-text-action"
                        onClick={() => setFormData({ ...formData, sku: generateRandomSku() })}
                      >
                        🎲 Auto-Gen
                      </button>
                    )}
                  </div>
                  <input
                    type="text"
                    required
                    value={formData.sku}
                    onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                    placeholder="e.g. ELE-8492"
                  />
                </div>

                <div className="form-group">
                  <label>Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  >
                    {CATEGORIES.filter((c) => c !== 'All Categories').map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group full">
                  <label>Product Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Industrial Solid State Relay 25A"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Stock Quantity</label>
                  <input
                    type="number"
                    min="0"
                    required
                    value={formData.quantity}
                    onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Safety Threshold (Min Alert)</label>
                  <input
                    type="number"
                    min="0"
                    required
                    value={formData.min_threshold}
                    onChange={(e) => setFormData({ ...formData, min_threshold: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Unit Price ($ USD)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    required
                    value={formData.unit_price}
                    onChange={(e) => setFormData({ ...formData, unit_price: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Warehouse Bay / Location</label>
                  <input
                    type="text"
                    placeholder="e.g. Zone B - Rack 04"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </div>

                <div className="form-group full">
                  <label>Supplier / Vendor Name</label>
                  <input
                    type="text"
                    placeholder="e.g. Omron Automation Corp"
                    value={formData.supplier}
                    onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setModalOpen(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingItem ? 'Save Updates' : 'Add to Catalog'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
