# Issue Reporting System for Local Communities

**Tech Stack:**  
- Backend: Django  
- Database: SQLite (development) → PostgreSQL (production)  
- Frontend: React (Vite) + Tailwind CSS + Axios 
- Media: Local `media/` folder (: Cloudinary later)  
- Version Control: Git/GitHub  

---

## Module 1: Project Setup & Core Models

### Task 1.1: Project Initialization
**Deliverable:** Repository with `/backend` and `/frontend` folders.
 
- **Backend**: Initialize Django, install `djangorestframework`, `django-cors-headers`, and `djangorestframework-simplejwt`.

- **Frontend**: Initialize Vite + React, install `axios`, `react-router-dom`, and `tailwind-css`.

- **Git**: Configure root `.gitignore` to skip `venv/`, `node_modules/`, and `.env`.

### Task 1.2: Database Models(DRF Focused)
**Deliverable:** All core models defined and migrated  

**users App:**  
`CustomUser` Model:
- **Fields**:
`email`: Unique identifier (Primary login).
`full_name`: User's display name.
`phone_number`: Unique, for SMS notifications.
`role`: ChoiceField (CITIZEN(DEFAULT), CELL_LEADER, SECTOR_LEADER, DISTRICT_LEADER).

`assigned_location_id`: Integer. Stores the ID from the external Rwanda API.
`supervisor`: Foreign Key (self). Links a Cell Leader to the Sector Leader who created them. 

- **Logic**: Implement a custom save() method or validation to ensure a District Leader can only create a Sector Leader.

**Reports App:**  
- **Issue** model  
  - Fields:  
    - `title`  
    - `description`  
    - `category`  
    - `location` (dropdown via Rwanda locations API: Province → District → Sector → Cell → Village)  
    - `reported_to` (stores **cell name**, not leader)  
    - `status` (default=Pending, In Progress, Reported to Higher Level, Solved)    
    - `comment` (latest leader comment)  
    - `photo` (ImageField)  
    - `citizen` (FK to Citizen)  
    - `created_at`, `updated_at` timestamps  


**General Requirements:**  
- All models have `__str__` methods  
- Database migrations applied successfully  
- Sample data can be created via Django shell 



**Locations App**:

*External API Proxy*
**Goal**: Connect to the Rwanda Administrative API.

Create a services.py to fetch Provinces, Districts, Sectors, and Cells.

Endpoints:
`/api/locations/districts/<province_id>/`
`/api/locations/sectors/<district_id>/`
`/api/locations/cells/<sector_id>/`

- **Frontend** (React): Build a reusable LocationSelector component with cascading dropdowns.


### Task 1.3: Admin Registration
**Deliverable:** All models accessible via Django admin  
**Acceptance Criteria:**  
- All models registered in `admin.py`  
- `Issue` model list display shows: `title`, `category`, `location`, `status`, `created_at`  
- User models show: `username`, `phone`, `address` / `assigned_location`  
- Superuser created for testing  
- Admin interface accessible and functional  

---

## Module 2: Authentication & User Management

### Task 2.1: User Registration
**Deliverable:** Citizens can register themselves  
**Acceptance Criteria:**  
- Registration form: `full name`, `email`, `password`, `confirm_password`, `phone`  
- Validation: required fields, email format, password match, min 8 characters  
- Successful registration creates user in DB and auto-login  
- Redirect: citizen → issue submission page  
- Leader registration **handled manually** by Admin/District/Sector as per hierarchy  
- Styled with Bootstrap/Tailwind  

### Task 2.2: Login & Logout
**Deliverable:** Users can login and logout  
**Acceptance Criteria:**  
- Login form: `username/email` + `password`  
- Invalid credentials show error  
- Logout clears session and redirects to homepage  
- Login required decorator works on protected views  

### Task 2.3: Access Control
**Deliverable:** Role-based access restrictions  
**Acceptance Criteria:**  
- **Auth**: JWT Token-based login.
- **Permissions**: Create DRF `BasePermission` classes to restrict API access based on `user.role`.
- **Frontend**: Implement `ProtectedRoutes` in React to redirect users to their specific dashboards.

- Citizens cannot access leader-only pages  
- Leaders cannot access citizen-only pages  
- Clear error message for unauthorized access  

### Task 2.4: Navigation & User Context
**Deliverable:** Dynamic navigation based on user state  
**Acceptance Criteria:**  
- Logged-out: Home, Submit Issue, Login, Register  
- Logged-in citizens: Home, Submit Issue, My Reports, Logout  
- Logged-in leaders: Home, Dashboard, Issues, Logout  
- User name displayed when logged in  
- Active page highlighted  
- Mobile-responsive menu  

---

## Module 3: Issue Submission & Management

### Task 3.1: Citizen Issue Submission
**Deliverable:** Citizens can submit issues  
**Acceptance Criteria:**  
- Form: `title`, `description`, `category`, `location` (cascading dropdown), optional `photo`  
- Status defaults to `Pending`  
- `comment` field **not included** in submission form  
- Success message shown; redirects to **My Reports**  
- Validation errors displayed inline  
- Styled with Tailwind  

### Task 3.2: Leader Dashboard
**Deliverable:** Leaders manage issues in their assigned location  
**Acceptance Criteria:**    
- Shows counts: total issues, pending, in progress, solved  
- Lists issues for assigned location only  
- Leaders can update: `status`, add `comment`  
- Filter by category, priority, status  
- Responsive layout  

- **Role-Based Data**: UI adapts based on role (e.g., Sector Leaders see an "Escalations" tab; Cell Leaders see a "New Reports" tab).

- **Status Management**: A simple "One-Click" update system (e.g., clicking a button to move an issue from "Pending" to "In Progress").

- **The Comment Thread**: Instead of just one comment, allow a small "Note" history so a Sector Leader can see why a Cell Leader escalated the issue.

- **Interactive Filters**: React-based filtering (no page reloads) by Category (Water, Road, etc.) and Date Range.

- **Urgency Indicator**: Highlight issues that haven't been touched for more than 48 hours.

### Task 3.3: Citizen My Reports Page
**Deliverable:** Citizens can track submitted issues  
**Acceptance Criteria:**  
- Shows issues submitted by logged-in user  
- Displays: `title`, `category`, `status`, `date`, latest leader `comment`  
- Link to detail page  
- Empty state: “No issues submitted yet”  

---

## Module 4: Media Management

### Task 4.1: Local Media Storage
**Deliverable:** Photos stored locally  
**Acceptance Criteria:**  
- `ImageField` stores images in `media/` folder  
- Accessible via URL in templates  
- `.gitignore` includes `media/`  

### Task 4.2: Cloudinary Integration (later)
**Deliverable:** Cloud storage for images  
**Acceptance Criteria:**  
- Cloudinary account created; API keys in `settings.py`  
- Image uploads go to Cloudinary; URLs stored in DB  
- Shared Cloudinary account for team  

---

## Module 5: Jurisdiction & Visibility Logic

### Task 5.1: Jurisdiction Validation & Filtering

**Deliverable**: Backend logic to enforce leader boundaries.

**Acceptance Criteria**: - API Mapping: Create a utility that maps the location_id from an Issue to the hierarchy (e.g., verifying that Village X belongs to Cell Y).

**Leader Filtering**: Implement get_queryset logic in the Reports API:

**Cell Leader**: Filter issues where location_id matches their assigned Cell.

**Sector Leader**: Filter issues where the location_id (Village) belongs to any Cell within their assigned Sector.

**Escalation Logic**: Ensure that when an issue is marked as "Reported to Higher Level," it becomes visible to the leader one step up in the hierarchy.

**Verification**: Prevent a Cell Leader from accidentally (or maliciously) viewing issues from a different Cell via the API.
---

## Module 6

🎨 `Design Guide for Figma`

**Colors**: Primary: #1B365D (Trust Blue), Action: #10B981 (Success Green).

**Style**: Use Cards for issues. A list of cards is much better for mobile citizens than a table.

**Components to Design**: Navbar (Dynamic), Status Badges (Colored), Image Preview Modal, Location Dropdown Group.