# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp
# import numpy as np

# # Define the points
# points = [
# (0.1294,-0.2228),
# (0,-0.2228),
# (-0.1294,-0.2228),
# (-0.0642,-0.1109),
# (0.0642,-0.1109),
# (0.1936,-0.1109),
# (0.2579,0),
# (0.1294,0),
# (0,0),
# (-0.1294,0),
# (-0.1936,0.1109),
# (0.1936,0.1109),
# (0.1294,0.2228),
# (0,0.2228),
# (-0.1294,0.2228),
# (0.0642,0.1109),
# (-0.0642,0.1109),
# (-0.2579,0),
# (-0.1936,-0.1109), 
# (0.87,-0.2228),
# (0.7406,-0.2228),
# (0.8058,-0.1109),
# (0.9342,-0.1109),
# (1.0636,-0.1109),
# (1.1279,0),
# (0.9994,0),
# (0.87,0),
# (0.7406,0),
# (0.6764,0.1109),
# (1.0636,0.1109),
# (0.9994,0.2228),
# (0.87,0.2228),
# (0.7406,0.2228),
# (0.9342,0.1109),
# (0.8058,0.1109),
# (0.6121,0),
# (0.6764,-0.1109),
# ]

# # Create the distance matrix
# def create_distance_matrix(points):
#     size = len(points)
#     dist_matrix = np.zeros((size, size))
#     for i in range(size):
#         for j in range(size):
#             if i != j:
#                 dist_matrix[i][j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
#     return dist_matrix

# distance_matrix = create_distance_matrix(points)

# # Create the routing index manager
# manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)

# # Create Routing Model
# routing = pywrapcp.RoutingModel(manager)

# def distance_callback(from_index, to_index):
#     # Returns the distance between the two nodes.
#     from_node = manager.IndexToNode(from_index)
#     to_node = manager.IndexToNode(to_index)
#     return int(distance_matrix[from_node][to_node])

# transit_callback_index = routing.RegisterTransitCallback(distance_callback)

# # Define cost of each arc
# routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# # Setting first solution heuristic
# search_parameters = pywrapcp.DefaultRoutingSearchParameters()
# search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

# # Solve the problem
# solution = routing.SolveWithParameters(search_parameters)

# # Get the route
# def get_solution(manager, routing, solution):
#     index = routing.Start(0)
#     plan_output = []
#     while not routing.IsEnd(index):
#         plan_output.append(manager.IndexToNode(index))
#         index = solution.Value(routing.NextVar(index))
#     plan_output.append(manager.IndexToNode(index))
#     return plan_output

# if solution:
#     optimal_route = get_solution(manager, routing, solution)
#     print("Optimal route:")
#     for node in optimal_route:
#         print(points[node])
# else:



# def convert_mdf4_to_csv(mdf4_file, csv_file1, csv_file2):
#     mdf = asammdf.MDF(mdf4_file)
    
#     # Extract data from MDF4 file
#     data = mdf.to_dataframe()
#     timestamps = mdf.get('Time').timestamps
    
#     # Write data to CSV file
#     with open(csv_file2, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Timestamp'])
#         writer.writerows(zip(timestamps))

#     data.to_csv(csv_file1, index=False)


# import numpy as np
# import matplotlib.pyplot as plt

# # Extract coordinates and commands
# commands = [
#     ("G01", -0.3343, 0),
#     ("G01", -0.2925, 0),
#     ("G02", -0.2925, 0, 0.2925),
#     ("G02", 0.2925, 0, 0.2925),
#     ("G01", 0.2925, 0),
#     # ("G01", 0.2925, 0),
#     ("G02", 0.3761, 0, 0.2925),
#     ("G02", 0.9611, 0, 0.2925),
#     ("G01", 0.9611, 0),
#     ("G02", 1.0447, 0, 0.2925),
#     ("G01", 1.6297, 0),
#     ("G02", 1.7133, 0, 0.2925),
#     ("G01", 2.2983, 0),
#     ("G02", 2.3819, 0, 0.2925),
#     ("G01", 2.9669, 0),
#     ("G02", 3.0505, 0, 0.2925),
#     ("G01", 3.6355, 0),
#     ("G02", 3.7191, 0, 0.2925),
#     ("G01", 4.3041, 0),
#     ("G02", 4.3877, 0, 0.2925),
#     ("G01", 4.9727, 0),
#     ("G02", 5.0563, 0, 0.2925),
#     ("G01", 5.6413, 0),
#     ("G02", 5.7249, 0, 0.2925),
#     ("G01", 6.3099, 0),
#     ("G02", 6.3935, 0, 0.2925),
#     ("G01", 6.9785, 0),
#     ("G02", 7.0621, 0, 0.2925),
#     ("G01", 7.6471, 0)
# ]

# # Initialize plot
# plt.figure(figsize=(12, 6))

# # Starting point
# current_x, current_y = -0.3343, 0
# plt.plot(current_x, current_y, 'go')  # Starting point marker

# # Plot each command
# for command in commands:
#     if command[0] == "G01":
#         _, x, y = command
#         plt.plot([current_x, x], [current_y, y], 'b-')
#         current_x, current_y = x, y
#     elif command[0] == "G02":
#         _, x, y, r = command
#         # Calculate center of the arc
#         dx = current_x - x
#         dy = current_y - y
#         q = np.sqrt(dx**2 + dy**2)
#         center_x = (current_x + x) / 2
#         center_y = (current_y + y) / 2
#         if dy == 0:
#             center_y += np.sqrt(r**2 - (q/2)**2)
#         else:
#             center_x += np.sqrt(r**2 - (q/2)**2)
#         # Calculate angles
#         angle1 = np.arctan2(current_y - center_y, current_x - center_x)
#         angle2 = np.arctan2(y - center_y, x - center_x)
#         if angle2 < angle1:
#             angle2 += 2 * np.pi
#         angles = np.linspace(angle1, angle2, 100)
#         arc_x = center_x + r * np.cos(angles)
#         arc_y = center_y + r * np.sin(angles)
#         plt.plot(arc_x, arc_y, 'r-')
#         current_x, current_y = x, y

# # Final plot adjustments
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('G-Code Path Visualization')
# plt.grid(True)
# plt.axis('equal')
# plt.show()

import os
import csv
import docx
from lxml import etree
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from tkinter import Tk, filedialog

# === CONFIG ===
trigger_text = "Presione retroceso al terminar de ver, o use las teclas f."

# === Get file from user ===
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Word Document",
        filetypes=[("Word Documents", "*.docx")]
    )
    return file_path

# === Extract list number (from w:numPr) ===
def get_numbering(paragraph):
    p = paragraph._p  # lxml element
    numPr = p.find(qn('w:numPr'))
    if numPr is None:
        return ""

    ilvl = numPr.find(qn('w:ilvl'))
    numId = numPr.find(qn('w:numId'))

    level = int(ilvl.get(qn('w:val'))) if ilvl is not None else 0
    num_id = int(numId.get(qn('w:val'))) if numId is not None else None

    if num_id is None:
        return ""

    # Since python-docx doesn't expose numbering text, return placeholder
    # like "• " for bullets or level-based indent markers
    return "  " * level + "- "

# === Extract lines after trigger ===
def extract_lines_after_trigger(doc_path, trigger):
    doc = docx.Document(doc_path)
    lines = []
    trigger_found = False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if trigger_found:
            prefix = get_numbering(para)
            lines.append(f"{prefix}{text}")
        elif trigger in text:
            trigger_found = True

    return lines

# === Write to CSV ===
def write_to_csv(file_name, lines, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for line in lines:
            writer.writerow([file_name, line])
    print(f"Saved to: {output_path}")

# === Main ===
if __name__ == "__main__":
    # docx_path = select_file()
    docx_path = r"C:\Users\akohli\Downloads\102A.docx"
    file_name = os.path.basename(docx_path)
    file_stem = os.path.splitext(file_name)[0]
    output_csv = os.path.join(os.path.dirname(docx_path), file_stem + ".csv")

    extracted_lines = extract_lines_after_trigger(docx_path, trigger_text)

    if not extracted_lines:
        print("No lines found after the trigger phrase.")
    else:
        write_to_csv(file_name, extracted_lines, output_csv)
