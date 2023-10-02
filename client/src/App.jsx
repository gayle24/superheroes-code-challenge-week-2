// src/App.jsx
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Home from './components/Home';
import Power from './components/Power';
import PowerEditForm from './components/PowerEditForm';
import Hero from './components/Hero';
import HeroPowerForm from './components/HeroPowerForm';

function App() {
  return (
    <Router>
      <div>
        <Header />
        <main>
          <Switch>
            <Route path="/powers/:id/edit" component={PowerEditForm} />
            <Route path="/powers/:id" component={Power} />
            <Route path="/heroes/:id" component={Hero} />
            <Route path="/hero_powers/new" component={HeroPowerForm} />
            <Route path="/" component={Home} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;
