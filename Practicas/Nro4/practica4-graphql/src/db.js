const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'admin',
  password: '123456',
  database: 'practica4_ventas'
});

module.exports = pool;
