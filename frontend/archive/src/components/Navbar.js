import React from 'react';
import { Link, useLocation } from 'react-router-dom';

/**
 * Navigation bar component for the application
 */
const Navbar = () => {
  const location = useLocation();
  
  // Check which path is active
  const isActive = (path) => {
    return location.pathname === path;
  };
  
  return (
    <nav style={{ 
      backgroundColor: '#333', 
      padding: '10px 20px',
      marginBottom: '20px'
    }}>
      <div style={{ 
        display: 'flex', 
        maxWidth: '1200px', 
        margin: '0 auto',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ color: 'white', fontWeight: 'bold', fontSize: '1.2rem' }}>
          YouTube Transcript Processor
        </div>
        
        <div>
          <Link 
            to="/" 
            style={{ 
              color: isActive('/') ? '#4CAF50' : 'white', 
              marginRight: '20px',
              textDecoration: 'none',
              fontWeight: isActive('/') ? 'bold' : 'normal'
            }}
          >
            Process Video
          </Link>
          
          <Link 
            to="/overview" 
            style={{ 
              color: isActive('/overview') ? '#4CAF50' : 'white',
              marginRight: '20px',
              textDecoration: 'none',
              fontWeight: isActive('/overview') ? 'bold' : 'normal'
            }}
          >
            Overview
          </Link>
          
          <Link 
            to="/downloads" 
            style={{ 
              color: isActive('/downloads') ? '#4CAF50' : 'white',
              textDecoration: 'none',
              fontWeight: isActive('/downloads') ? 'bold' : 'normal'
            }}
          >
            Downloads
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;