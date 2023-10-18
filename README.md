# ICU Monitor Signal Viewer

ICU Monitor Signal Viewer is a desktop application built with Python that enables users to load and display signals from various channels. The application utilizes PyQt5, pyqtgraph, pyautogui, and PIL to offer a feature-rich and user-friendly signal visualization experience. With ICU Monitor Signal Viewer, users can analyze signals, manipulate their appearance, create reports, and perform data analysis.

## Features

- **Signal Loading and Display**: The application allows users to load signals from different channels and displays them on graph widgets. Users can easily navigate through the loaded signals and visualize them in real-time.

- **Play/Pause Signals**: Users have control over the playback of signals. They can play or pause the signals according to their requirements, enabling them to focus on specific instances or time intervals.

- **Signal Color Customization**: Users can customize the color of each signal on the graph. This feature enables better differentiation and visualization of multiple signals.

- **Signal Legend**: The application provides an option for users to add legends for each signal on the graph. This allows users to identify and understand the meaning of each signal more easily.

- **Multiple Graph Widgets**: ICU Monitor Signal Viewer supports the display of multiple signals on separate graph widgets. Users can compare and analyze signals from different channels simultaneously, offering a comprehensive view of the data.

- **Signal Manipulation**: Users can move signals from one graph widget to another, facilitating comparison and analysis. This feature enhances the flexibility and adaptability of the application.

- **Signal Snapshots**: Users can capture snapshots of signals at specific instances. This functionality allows users to save and reference important moments or noteworthy data points.

- **PDF Report Generation**: The application enables users to create PDF reports that include snapshots of signals and data analysis. Users can generate comprehensive reports that provide a visual representation of the data along with statistical analysis.

- **Data Analysis**: ICU Monitor Signal Viewer incorporates data analysis capabilities. Users can calculate essential statistical parameters such as mean, minimum, maximum, standard deviation, and duration for each signal. This feature simplifies the process of extracting valuable insights from the data.

## Prerequisites

- Python 3.7 or above
- PyQt5
- pyqtgraph
- pyautogui
- PIL

## Installation

1. Clone the repository:
   ````
   git clone https://github.com/MoHazem02/Signal-Viewer.git
   ```

2. Install the required dependencies using pip:
   ````
   pip install pyqt5 pyqtgraph pyautogui pillow
   ```

## Usage

1. Navigate to the project directory:
   ````
   cd icu-monitor-signal-viewer
   ```

2. Run the application:
   ````
   python main.py
   ```

3. Load signals from the desired channels using the application's interface.

4. Play, pause, and customize the appearance of the signals as needed.

5. Utilize the multiple graph widgets to compare and analyze signals.

6. Move signals between graph widgets to facilitate comparison.

7. Capture snapshots of signals at specific instances for reference.

8. Generate PDF reports that include snapshots and data analysis.

## Contributing

Contributions to ICU Monitor Signal Viewer are welcome! If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.

When contributing, please ensure that you follow the existing coding style and include clear commit messages to maintain a well-documented project history.


## Acknowledgments

We would like to thank the developers and contributors of PyQt5, pyqtgraph, pyautogui, and PIL for their excellent libraries, which made this project possible.

