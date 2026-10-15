import React, { useState, useEffect } from 'react';

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
  const [health, setHealth] = useState({ status: 'checking', version: '-' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    quantity: 0,
    min_threshold: 10,
    unit_price: 0.0,
    supplier: '',
    location: '',
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Build query string
      const params = new URLSearchParams();
      if (search) params.append('q', search);
      if (selectedCategory !== 'All Categories') params.append('category', selectedCategory);
      if (statusFilter !== 'ALL') params.append('stock_status', statusFilter.toLowerCase());

      const [itemsRes, statsRes, healthRes] = await Promise.all([
        fetch(`/api/inventory?${params.toString()}`),
        fetch('/api/inventory/stats'),
        fetch('/health'),
      ]);

      if (!itemsRes.ok) throw new Error(`API Error: ${itemsRes.status}`);

      const itemsData = await itemsRes.json();
      const statsData = statsRes.ok ? await statsRes.json() : stats;
      const healthData = healthRes.ok ? await healthRes.json() : { status: 'offline' };

      setItems(itemsData);
      setStats(statsData);
      setHealth(healthData);
    } catch (err) {
      console.error('Fetch error:', err);
      setError('Unable to reach StockPulse Backend. Please ensure the backend service is running.');
      setHealth({ status: 'offline', version: '-' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [search, selectedCategory, statusFilter]);

  const handleOpenCreateModal = () => {
    setEditingItem(null);
    setFormData({
      sku: `SKU-${Math.floor(1000 + Math.random() * 9000)}`,
      name: '',
      category: 'Electronics',
      quantity: 15,
      min_threshold: 10,
      unit_price: 25.0,
      supplier: '',
      location: 'Warehouse A - Bay 1',
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
      fetchData();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this inventory item?')) return;
    try {
      const res = await fetch(`/api/inventory/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete item');
      fetchData();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">SP</div>
          <span className="brand-name">StockPulse</span>
        </div>

        <ul className="nav-links">
          <li className="nav-item active">📦 Inventory Catalog</li>
          <li className="nav-item">📊 Analytics & KPIs</li>
          <li className="nav-item">🚚 Suppliers</li>
          <li className="nav-item">⚙️ DevOps Settings</li>
        </ul>

        <div className="system-status-box">
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '6px' }}>
            <span
              className="status-dot"
              style={{
                backgroundColor: health.status === 'up' ? '#10b981' : '#ef4444',
                boxShadow:
                  health.status === 'up'
                    ? '0 0 8px #10b981'
                    : '0 0 8px #ef4444',
              }}
            />
            <span style={{ fontWeight: 600 }}>Backend Status: {health.status.toUpperCase()}</span>
          </div>
          <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>
            Environment: Docker / Kubernetes<br />
            API Version: {health.version || '1.0.0'}
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <div className="top-bar">
          <div>
            <h1>Warehouse Inventory Control</h1>
            <p>Live synchronized 3-tier catalog connecting PostgreSQL & FastAPI</p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button className="btn btn-secondary" onClick={fetchData}>
              🔄 Refresh
            </button>
            <button className="btn btn-primary" onClick={handleOpenCreateModal}>
              ➕ Add Item
            </button>
          </div>
        </div>

        {error && (
          <div
            style={{
              backgroundColor: '#ef444422',
              color: '#f87171',
              padding: '1rem',
              borderRadius: '8px',
              marginBottom: '1.5rem',
              border: '1px solid #ef444444',
            }}
          >
            ⚠️ {error}
          </div>
        )}

        {/* Live KPI Metric Cards */}
        <section className="kpi-grid">
          <div className="kpi-card">
            <div className="label">Total SKUs</div>
            <div className="value">{stats.total_skus}</div>
            <div className="subtext">Unique catalog items registered</div>
          </div>
          <div className="kpi-card">
            <div className="label">Total Units on Hand</div>
            <div className="value">{stats.total_units.toLocaleString()}</div>
            <div className="subtext">Across all warehouse locations</div>
          </div>
          <div className="kpi-card">
            <div className="label">Inventory Valuation</div>
            <div className="value">
              ${stats.total_valuation.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </div>
            <div className="subtext">Total asset replacement value</div>
          </div>
          <div className="kpi-card">
            <div className="label">Stock Alerts</div>
            <div className="value" style={{ color: stats.low_stock_count > 0 ? '#f59e0b' : '#10b981' }}>
              {stats.low_stock_count} <span style={{ fontSize: '1rem', color: '#9ca3af' }}>/ {stats.out_of_stock_count} OOS</span>
            </div>
            <div className="subtext">{stats.low_stock_count} below min threshold</div>
          </div>
        </section>

        {/* Filter and Search Bar */}
        <div className="filter-bar">
          <input
            type="text"
            className="search-input"
            placeholder="Search by name or SKU..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

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
            {['ALL', 'IN_STOCK', 'LOW_STOCK', 'OUT_OF_STOCK'].map((st) => (
              <button
                key={st}
                className={`status-pill ${statusFilter === st ? 'active' : ''}`}
                onClick={() => setStatusFilter(st)}
              >
                {st.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        {/* Inventory Data Table */}
        <div className="table-container">
          {loading ? (
            <div className="empty-state">Loading warehouse records...</div>
          ) : items.length === 0 ? (
            <div className="empty-state">
              No inventory records found. Click "Add Item" to create one!
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Product Name</th>
                  <th>Category</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Total Value</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th style={{ textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id}>
                    <td style={{ fontFamily: 'monospace', fontWeight: 600 }}>{item.sku}</td>
                    <td>
                      <div style={{ fontWeight: 600 }}>{item.name}</div>
                      {item.supplier && (
                        <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{item.supplier}</div>
                      )}
                    </td>
                    <td>{item.category}</td>
                    <td>
                      <div style={{ fontWeight: 600 }}>{item.quantity}</div>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                        Min: {item.min_threshold}
                      </div>
                    </td>
                    <td>${item.unit_price.toFixed(2)}</td>
                    <td style={{ fontWeight: 600 }}>
                      ${(item.quantity * item.unit_price).toFixed(2)}
                    </td>
                    <td style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
                      {item.location || 'Unassigned'}
                    </td>
                    <td>
                      <span className={`badge badge-${item.status}`}>
                        {item.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '0.5rem' }}>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.35rem 0.65rem', fontSize: '0.8rem' }}
                          onClick={() => handleOpenEditModal(item)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '0.35rem 0.65rem', fontSize: '0.8rem' }}
                          onClick={() => handleDelete(item.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>

      {/* Add / Edit Modal */}
      {modalOpen && (
        <div className="modal-overlay" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingItem ? 'Edit Inventory Item' : 'Add New Inventory Item'}</h2>
              <button className="close-btn" onClick={() => setModalOpen(false)}>
                &times;
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>SKU Code</label>
                  <input
                    type="text"
                    required
                    value={formData.sku}
                    onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
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
                  <label>Min Alert Threshold</label>
                  <input
                    type="number"
                    min="0"
                    required
                    value={formData.min_threshold}
                    onChange={(e) => setFormData({ ...formData, min_threshold: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Unit Price ($)</label>
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
                  <label>Warehouse Location</label>
                  <input
                    type="text"
                    placeholder="e.g. Bay 4 - Shelf C"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  />
                </div>

                <div className="form-group full">
                  <label>Supplier / Vendor</label>
                  <input
                    type="text"
                    placeholder="e.g. Acme Components LLC"
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
                  {editingItem ? 'Save Changes' : 'Create Item'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
