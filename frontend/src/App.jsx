import React from 'react'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { Grid, Header } from 'semantic-ui-react'

import '@/src/App.css'
import 'semantic-ui-css/semantic.min.css'

import AppLogo from '@/src/components/AppLogo'
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
      <div className='app-container'>
        {/* Full width header */}
        <Header as='header' fixed='top' className='custom-header'>
          <Grid>
            <Grid.Row verticalAlign='middle'>
              <Grid.Column computer={4} tablet={16} mobile={16}>
                <AppLogo />
              </Grid.Column>
              <Grid.Column computer={12} tablet={16} mobile={16}>
                <Navbar />
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Header>

        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/cranes/:id' element={<CraneDetail />} />
          <Route path='/compare' element={<ComparisonTable />} />
          <Route path='/history' element={<CalcHistory />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
