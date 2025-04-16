import React from 'react'
import { NavLink } from 'react-router-dom'
import { Menu } from 'semantic-ui-react'

const Navbar = () => (
  <Menu pointing secondary>
    <Menu.Item as={NavLink} exact to='/' name='Home' />
    <Menu.Item as={NavLink} to='/comparison_table' name='Comparison Table' />
    <Menu.Item as={NavLink} to='/calc_history' name='Calculation History' />
    <Menu.Item as={NavLink} to='/about' name='About' />
  </Menu>
)

export default Navbar
