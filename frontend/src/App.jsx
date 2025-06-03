import { useState, useEffect } from 'react';
import './App.css';
import CompanyForm from './components/CompanyForm';
import CompanyList from './components/CompanyList';

function App() {
  const [companies, setCompanies] = useState([]);
  const [editingCompany, setEditingCompany] = useState(null);

  const fetchCompanies = async () => {
    try {
      const response = await fetch('http://localhost:8000/companies');
      if (!response.ok) throw new Error(await response.text());
      const data = await response.json();
      setCompanies(data);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleAddCompany = async (company) => {
    try {
      const response = await fetch('http://localhost:8000/companies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(company),
      });
      if (!response.ok) throw new Error(await response.text());
      await fetchCompanies();
    } catch (error) {
      console.error('Error adding company:', error);
    }
  };

  const handleEditCompany = async (company) => {
    try {
      const response = await fetch(`http://localhost:8000/companies/${company.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(company),
      });
      if (!response.ok) throw new Error(await response.text());
      await fetchCompanies();
      setEditingCompany(null);
    } catch (error) {
      console.error('Error updating company:', error);
    }
  };

  const handleDeleteCompany = async (companyId) => {
    try {
      const response = await fetch(`http://localhost:8000/companies/${companyId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error(await response.text());
      await fetchCompanies();
    } catch (error) {
      console.error('Error deleting company:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Company Management</h1>
      <CompanyForm
        onSubmit={editingCompany ? handleEditCompany : handleAddCompany}
        editingCompany={editingCompany}
        setEditingCompany={setEditingCompany}
      />
      <CompanyList
        companies={companies}
        onEdit={setEditingCompany}
        onDelete={handleDeleteCompany}
      />
    </div>
  );
}

export default App;