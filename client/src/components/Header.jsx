import { Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <h1>
        <Link to="/heroes">Super Heroes</Link>
      </h1>
    </header>
  );
}

export default Header;