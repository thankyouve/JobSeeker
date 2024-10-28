import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <h1>JobSeeker</h1>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/add-company">Add Company</Link>
        <Link to="/company-list">Monitored Career Pages</Link>
      </nav>
    </header>
  );
};

export default Header;
