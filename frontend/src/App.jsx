import React from 'react'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { Container, Header } from 'semantic-ui-react'

import 'semantic-ui-css/semantic.min.css'
import '@/src/App.css'

import Navbar from '@/src/components/Navbar'
import About from '@/src/pages/About'
import CalcHistory from '@/src/pages/CalcHistory'
import ComparisonTable from '@/src/pages/ComparisonTable'
import CraneDetail from '@/src/pages/CraneDetail'
import Home from '@/src/pages/Home'

function App() {
  return (
    /* Router container to handle the routing */
    <Router>
      {/* Main layout container */}
      <Container>
        <Header as='header'>
          <Navbar />
        </Header>

        {/* Routes available in the app */}
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/cranes/:id' element={<CraneDetail />} />
          <Route path='/comparison_table' element={<ComparisonTable />} />
          <Route path='/calc_history' element={<CalcHistory />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </Container>
    </Router>
  )
}

export default App
