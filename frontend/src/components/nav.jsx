// @flow
import React from 'react'
import { Nav, Navbar, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'

type Props = {}

class NavBar extends React.Component<Props> {
    // handleSelect(event: SyntheticInputEvent<HTMLInputElement>) {
    // handleSelect(eventKey: string) {
    //     // event.preventDefault()
    //     alert(`selected ${eventKey}`)
    // }

    render() {
        return (
            <Navbar fixedTop collapseOnSelect>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="/">Lil Data</a>
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav bsStyle='tabs' activeKey='1'>
                        <NavItem eventKey='1' href='/Lil-Data'>
                            Do
                        </NavItem>
                        <NavItem eventKey='2' href='#kkk'>
                            Not
                        </NavItem>
                        <NavItem eventKey='3' href='/charts'>
                            Not
                        </NavItem>
                        <NavDropdown eventKey='4' title='Dropdown' id='nav-dropdown'>
                            <MenuItem eventKey='4.1'>Because</MenuItem>
                            <MenuItem eventKey='4.2'>they</MenuItem>
                            <MenuItem eventKey='4.3'>do</MenuItem>
                            <MenuItem divider />
                            <MenuItem eventKey='4.4'>nothing</MenuItem>
                        </NavDropdown>
                    </Nav>
                    <Nav pullRight>
                        <NavItem eventKey={1} href="https://github.com/harrisonxia/Lil-Data">
                            <b>Show me the code</b>
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
                )
    }
}

// render(<NavDropdownExample />)

export default NavBar