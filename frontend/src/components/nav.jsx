// @flow
import React from 'react'
import { Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'

type Props = {}

class NavBar extends React.Component<Props> {
    // handleSelect(event: SyntheticInputEvent<HTMLInputElement>) {
    handleSelect(eventKey: string) {
        // event.preventDefault()
        alert(`selected ${eventKey}`)
    }

    render() {
        return (
            <Nav bsStyle='tabs' activeKey='1' onSelect={k => this.handleSelect(k)}>
                <NavItem eventKey='1' href='/Lil-Data'>
                    Do
                </NavItem>
                <NavItem eventKey='2' title='Item'>
                    Not
                </NavItem>
                <NavItem eventKey='3' disabled>
                    Click
                </NavItem>
                <NavDropdown eventKey='4' title='Dropdown' id='nav-dropdown'>
                    <MenuItem eventKey='4.1'>Because</MenuItem>
                    <MenuItem eventKey='4.2'>they</MenuItem>
                    <MenuItem eventKey='4.3'>do</MenuItem>
                    <MenuItem divider />
                    <MenuItem eventKey='4.4'>nothing</MenuItem>
                </NavDropdown>
            </Nav>
        )
    }
}

// render(<NavDropdownExample />)

export default NavBar