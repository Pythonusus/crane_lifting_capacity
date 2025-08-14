/**
 * Component containing app logo and app title
 * @module components/AppLogo
 */

import React from 'react'

import logo from '@/src/assets/app_logo.png'
import './AppLogo.css'

const AppLogo = () => {
  return (
    <div className='app-logo-container'>
      <img
        src={logo}
        alt='Crane lifting capacity calculator logo'
        className='app-logo '
      />
      <div className='app-title'>
        <span>Калькулятор</span>
        <span>грузоподъемности</span>
        <span>кранов</span>
      </div>
    </div>
  )
}

export default AppLogo
