import React from 'react'
import { NavLink } from 'react-router-dom'
import { Menu, Icon } from 'semantic-ui-react'
import './Navbar.css'

const Navbar = () => (
  <Menu as='nav' className='custom-navbar' pointing secondary>
    <Menu.Item as={NavLink} exact to='/'>
      <Icon name='cog' size='large' />
      <span className='font-size-4 hide-on-tablet'>Выбрать кран</span>
    </Menu.Item>
    <Menu.Item as={NavLink} to='/compare'>
      <Icon name='table' size='large' />
      <span className='font-size-4 hide-on-tablet'>Таблица сравнения</span>
    </Menu.Item>
    <Menu.Item as={NavLink} to='/history'>
      <Icon name='history' size='large' />
      <span className='font-size-4 hide-on-tablet'>История расчетов</span>
    </Menu.Item>
    <Menu.Item as={NavLink} to='/about'>
      <Icon name='info circle' size='large' />
      <span className='font-size-4 hide-on-tablet'>О программе</span>
    </Menu.Item>
  </Menu>
)

export default Navbar
