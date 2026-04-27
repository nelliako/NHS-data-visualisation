# NHS-data-visualisation
Link to Tableau: https://public.tableau.com/app/profile/nellia.kornilova/viz/NHSdataChapter5overview/Maindashboard 

## Data exploration and preparation

### Visual Design Type: 
Parallel Coordinates plot

### Focus Cohort: Years, Age Groups, and/or Genders: 
The years (time period) of hospital admissions shown: 1998-2024
the age groups shown: entire population
genders: entire population

### Variables:
Diagnostic Groups Descriptions 
Year
Mean Age
Percentage Male 
Percentage Female
Total FCE
Waiting list (size)
Mean waiting time (days)
Percentage Day Cases
Percentage Emergency Cases
Mean length of stay

Justification:

I chose them because I aimed at creating a comprehensive 360-degree view of the NHS Mental Health service. By including these variables, the visualisation tells a complete story of the patient journey: from who the patients are to how they enter the system and how long they stay.


#### The demographic profile (Mean Age, % Male, % Female):

These attributes were chosen to establish the clinical who for each diagnosis.
By mapping Age and Gender, the chart reveals clinical special clinical features, such as the pediatric focus of developmental disorders versus the geriatric focus of organic disorders.


#### Operational demand and access (Total FCEs, Waiting List Size, Mean Wait Time)

These variables were chosen to measure the systemic pressure on the NHS.

-Total FCE (Volume): chosen to distinguish between high-volume mass services (like Mood Disorders) and low-volume specialised services.

-Waiting List (size - patients & number of days): these are the primary indicators of access barriers. Including both allows the viewer to see the waiting time problem, where a condition might have a small waiting list but a long waiting time, which is a much more critical insight than list size alone.


#### Care pathway and intensity (% Day Cases, % Emergency, Mean LOS)

These attributes were chosen to evaluate the realities and cost of care.

-Day Case & Emergency %: this tells if a service is proactive (planned day cases) or reactive (emergency admissions). High emergency rates usually signal a system under stress or a lack of community-based prevention.

-Mean Length of Stay (LOS): this was chosen as the measure of clinical severity and resource consumption. 

### Visual mappings:
#### position (x, y axes) 

-X-Axis - mapped to Measure Names. Each position represents a distinct NHS metric (e.g., Mean Age, Wait Times, Length of Stay).

-Y-Axis - mapped to Measure Values. Each point on the vertical line represents the magnitude of that metric. These are normalised (scaled 0 to 1) to allow for the comparison of different units (years vs. days vs. percentages) on a single shared plane.

#### color 

-Overview ("all") - mapped to a categorical palette, where each unique colour represents a specific Diagnostic Chapter.
-Highlight (specific selection) - mapped to a binary palette. A high-contrast red is mapped to the "Selected" chapter, while a neutral light grey is mapped to "Background" data to reduce visual noise.

#### path

-Path (line) - mapped to Chapter Description. This connects the individual data points across the X-axis to form a continuous line. 
hierarchy & interaction
-Parameter control - determines which data mark is brought to the front of the visualisation, the "Selected" red line is forced to the top of the screen so it is never obscured by the grey background lines.
-Dynamic visibility - the colour legend is mapped to the Parameter state, appearing or changing only when "All" diagnostic groups are chosen.

### Unique Observation: 
My visualisation focuses on 3 questions:

#### Q1 - How do patient demographics differ across various mental health diagnosis groups? 

-One of the observations is the age divergence: when looking at “All” diagnoses in “All” years, there is a clear split. At the very top of the Mean Age axis, there is Organic Mental Disorders (Dementia/Alzheimer's), representing an elderly demographic. Conversely, Disorders of psychological development (including Autism/ADHD) appear at the bottom of the axis, identifying them as pediatric-heavy services. [0:25]

-There is an interesting crossing between Male % and Female % axis on “All” diagnosis groups and “All” years view which shows there are certain conditions that are more profound in male or female population. For example, Mood affective disorders seem to affect the female population (40%) more than the male (60%) on average. [0:40]

#### Q2 - Which conditions face the most significant barriers to access, and how does that impact their treatment?

-With Schizophrenia in “All” years, it averages an 80-day wait and a 61-day stay. The visualisation shows that these patients face one of the highest barriers and require long recoveries. It could be possible that these 80 days of waiting allow symptoms to become more acute, thereby inflating the length of stay once they finally reach a bed. [1:27]

-The parallel coordinates plot reveals that waitlist size is often a poor proxy for service efficiency. This bottleneck is visually proven when the Wait Time line sits significantly higher than List Size. This justifies that simply reducing the number of people on a list won't improve services where delays are driven by clinical complexity rather than administrative backlogs. Again with the Schizophrenia line overtakes other chapters by climbing from an average list size to a 80-day wait, proving the system requires increased specialised bed capacity and assessment approach, not just a shorter waiting list. [1:05]

#### Q3 - Is the care for this specific diagnosis primarily planned (Day cases) or reactive (Emergency cases)?

-There is a visible V-shape between Day cases % and Emergency cases % axis in “All” year and “All” diagnostic groups: very few lines sit high on the Day Case axis. Most lines will dip at Day Cases and spike at Emergency Cases. This could be a sign that the NHS mental health system is reactive. Mood [affective] disorders and Schizophrenia typically show an “inverted V", meaning they have nearly 0% planned day cases and over 50–60% emergency admissions. [1:20]

### Data Preparation: 
I used Python scripts to extract Chapter 5 codes across all years and collect them all in one spreadsheet in formats suitable for Parallel Coordinates plot and supplementary visualisations. I also normalised all the values in Tableau.

### URL to screen-capture demo:

Link to video: https://www.loom.com/share/394682c7a02f4a98b818bc5495e66c1d 




