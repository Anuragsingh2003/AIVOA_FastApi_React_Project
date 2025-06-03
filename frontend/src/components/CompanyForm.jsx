import React, { useState, useEffect } from 'react';

function CompanyForm({ onSubmit, editingCompany, setEditingCompany }) {
  const [formData, setFormData] = useState({ name: '', location: '' });

  useEffect(() => {
    if (editingCompany) {
      setFormData({
        name: editingCompany.name,
        location: editingCompany.location,
        id: editingCompany.id,
      });
    } else {
      setFormData({ name: '', location: '' });
    }
  }, [editingCompany]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      ...(editingCompany && { id: editingCompany.id }),
    });
    if (!editingCompany) {
      setFormData({ name: '', location: '' });
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-semibold mb-2">
        {editingCompany ? 'Edit Company' : 'Add Company'}
      </h2>
      <div className="space-y-4">
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Company Name"
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          placeholder="Location"
          className="w-full p-2 border rounded"
          required
        />
        <div>
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            {editingCompany ? 'Update' : 'Add'}
          </button>
          {editingCompany && (
            <button
              onClick={() => setEditingCompany(null)}
              className="ml-2 bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default CompanyForm;