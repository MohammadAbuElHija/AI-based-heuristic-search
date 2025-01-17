# Wizard Pathfinding Game with AI Navigation

## Description
This project is a grid-based strategy game where players control wizards, including Harry Potter, to destroy Horcruxes and defeat Voldemort while navigating a dynamic map. The game features complex mechanics such as impassable tiles, cyclically moving Death Eaters, multi-agent coordination, and survival strategies. The goal is to ensure all wizards survive, complete objectives, and optimize paths using AI.

## Key Features
- **AI Pathfinding**: Implemented the A* algorithm with custom heuristic functions for efficient navigation around obstacles and enemies.
- **Dynamic Obstacles**: Integrated mechanics to handle cyclic enemy movements and impassable tiles.
- **Multi-Agent Coordination**: Managed multiple wizards with unique tasks, ensuring survival and task completion.
- **Game Rules**: Wizards must destroy Horcruxes before defeating Voldemort, with game-over conditions tied to survival mechanics.
- **Testing**: Designed 48 unique test scenarios to validate algorithm performance under different configurations.

## Technologies Used
- Python for algorithm implementation and game logic.
- Custom heuristics for balancing path efficiency, obstacle handling, and survival strategies.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/wizard-pathfinding-game.git
   cd wizard-pathfinding-game
