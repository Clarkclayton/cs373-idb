var Navbar = ReactBootstrap.Navbar,
    Nav = ReactBootstrap.Nav,
    NavItem = ReactBootstrap.NavItem,
    NavDropdown = ReactBootstrap.NavDropdown,
    MenuItem = ReactBootstrap.MenuItem;

const navbarInstance = (
<Navbar inverse style={{ borderRadius: '0px' }}>
  <Navbar.Header>
    <Navbar.Brand>
      <a href="#">SWECune</a>
    </Navbar.Brand>
    <Navbar.Toggle />
  </Navbar.Header>
  <Navbar.Collapse>
    <Nav>
      <NavItem eventKey={1} href="#">Pokemon</NavItem>
      <NavItem eventKey={2} href="#">Item</NavItem>
      <NavItem eventKey={3} href="#">Locations</NavItem>
    </Nav>
  </Navbar.Collapse>
</Navbar>
);

ReactDOM.render(navbarInstance, document.getElementById("navbar"));
