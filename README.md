# Travel Planner API

Backend REST API for managing travel projects and places.


### Travel Projects
- Create travel projects (title, notes, start date)
- List, retrieve, update, delete projects
- Prevent deletion if any place is marked as visited
- Auto-calculated `is_completed` status

### Places
- Add places to a travel project
- Bulk create places during project creation
- Validate places via external API (Art Institute of Chicago)
- Prevent duplicate places per project
- Mark places as visited
- Update notes for places
- List and retrieve places per project

## ⚙️ Setup
git clone https://github.com/Luntik7/TravelProject.git
cd TravelProject
python -m venv venv
venv\scripts\activate
pip install -r requirements.txt
python manage.py runserver
