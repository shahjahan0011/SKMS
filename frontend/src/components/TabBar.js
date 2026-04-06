function TabBar({ tabs, activeTab, onTabChange }) {
  return (
    <nav className="tab-bar" aria-label="Primary navigation">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={tab.id === activeTab ? "tab active" : "tab"}
          onClick={() => onTabChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
}

export default TabBar;
