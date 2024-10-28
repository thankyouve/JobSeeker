import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import AddCompanyPage from './pages/AddCompanyPage';
import CompanyList from './components/CompanyList';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/add-company" element={<AddCompanyPage />} />
        <Route path="/company-list" element={<CompanyList />} />
      </Routes>
    </Router>
  );
};

export default App;
