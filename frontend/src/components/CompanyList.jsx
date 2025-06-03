import React from 'react';

function CompanyList({ companies, onEdit, onDelete }) {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-2">Companies</h2>
      {companies.length === 0 ? (
        <p>No companies found.</p>
      ) : (
        <ul className="space-y-2">
          {companies.map((company) => (
            <li key={company.id} className="p-4 border rounded flex justify-between">
              <div>
                <p><strong>Name:</strong> {company.name}</p>
                <p><strong>Location:</strong> {company.location}</p>
              </div>
              <div>
                <button
                  onClick={() => onEdit(company)}
                  className="bg-yellow-500 text-white p-2 rounded mr-2 hover:bg-yellow-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => onDelete(company.id)}
                  className="bg-red-500 text-white p-2 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default CompanyList;