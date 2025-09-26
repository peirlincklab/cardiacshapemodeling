# deformetrica_utils.py

"""
Utility functions for generating Deformetrica configuration files:
- data_set.xml
- model.xml
- optimization_parameters.xml

Dependencies:
- xml.etree.ElementTree
- os
- glob
"""

import os
import glob
from xml.etree.ElementTree import Element, SubElement, ElementTree


def generate_xml_data(data_folder):
    data_set = Element('data-set')

    for file_path in sorted(glob.glob(os.path.join(data_folder, '*.vtk'))):
        subject = SubElement(data_set, 'subject', id=os.path.splitext(os.path.basename(file_path))[0])
        obj = SubElement(subject, 'object', id='biventricular')
        obj.text = file_path

    return data_set


def generate_xml_model(kernel_width, cp_spacing, k_type="keops", k_device="gpu"):
    model = Element("model")

    deformation = SubElement(model, "deformation")
    SubElement(deformation, "kernel-width").text = str(kernel_width)
    SubElement(deformation, "kernel-type").text = k_type
    SubElement(deformation, "kernel-device").text = k_device

    attachments = SubElement(model, "attachments")
    attachment = SubElement(attachments, "attachment", object_id="biventricular")
    SubElement(attachment, "weight").text = "1.0"
    SubElement(attachment, "kernel-width").text = str(kernel_width)

    cp = SubElement(model, "initial-control-points")
    SubElement(cp, "use-bounding-box").text = "true"
    SubElement(cp, "point-spacing").text = str(cp_spacing)

    return model


def generate_xml_optimization(converge_tol=1e-5, max_iter=150, optimization_method="scipy-lbfgsb"):
    optimization = Element("optimization-parameters")
    SubElement(optimization, "max-iterations").text = str(max_iter)
    SubElement(optimization, "convergence-tolerance").text = str(converge_tol)
    SubElement(optimization, "optimizer-type").text = optimization_method
    return optimization


def save_xml(xml_element, file_path):
    tree = ElementTree(xml_element)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print(f"Saved XML to {file_path}")
