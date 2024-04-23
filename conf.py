import tkinter as tk
from tkinter import filedialog, messagebox
import os
import csv
import json
import yaml
import xml.etree.ElementTree as ET

def obtenir_extension_fichier(chemin_fichier):
    """Fonction pour obtenir l'extension d'un fichier."""
    _, extension = os.path.splitext(chemin_fichier)
    return extension

def convertir_en_csv(chemin_fichier_entree, chemin_fichier_sortie, delimiteur=','):
    with open(chemin_fichier_entree, 'r', encoding='utf-8') as fichier_entree:
        lignes = fichier_entree.readlines()

        # Supprimer les caractères de saut de ligne des lignes
        lignes = [ligne.strip() for ligne in lignes]

        # Écrire les lignes dans un fichier CSV
        with open(chemin_fichier_sortie, 'w', newline='', encoding='utf-8') as fichier_sortie:
            writer = csv.writer(fichier_sortie, delimiter=delimiteur)
            for ligne in lignes:
                # Diviser chaque ligne en colonnes en utilisant le délimiteur spécifié
                colonnes = ligne.split(delimiteur)
                writer.writerow(colonnes)

def convertir_en_json(chemin_fichier_entree, chemin_fichier_sortie):
    with open(chemin_fichier_entree, 'r', encoding='utf-8') as fichier_entree:
        donnees = fichier_entree.read()
        objets = [ligne.split('\t') for ligne in donnees.split('\n') if ligne]  # Supprime les lignes vides et divise chaque ligne en objets
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as fichier_sortie:
            json.dump(objets, fichier_sortie, indent=4)

def convertir_en_yaml(chemin_fichier_entree, chemin_fichier_sortie):
    with open(chemin_fichier_entree, 'r', encoding='utf-8') as fichier_entree:
        donnees = fichier_entree.read()
        objets = [ligne.split('\t') for ligne in donnees.split('\n') if ligne]  # Supprime les lignes vides et divise chaque ligne en objets
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as fichier_sortie:
            yaml.dump(objets, fichier_sortie, default_flow_style=False)

def convertir_en_xml(chemin_fichier_entree, chemin_fichier_sortie):
    racine = ET.Element("data")
    with open(chemin_fichier_entree, 'r', encoding='utf-8') as fichier_entree:
        for index, ligne in enumerate(fichier_entree):
            elements = ligne.strip().split("\t")
            element = ET.SubElement(racine, "item", id=str(index+1))
            for e in elements:
                sous_element = ET.SubElement(element, "value")
                sous_element.text = e

    arbre = ET.ElementTree(racine)
    arbre.write(chemin_fichier_sortie)

def afficher_extension():
    global chemin_fichier_selectionne
    chemin_fichier_selectionne = filedialog.askopenfilename(initialdir="/", title="Sélectionner le fichier", filetypes=(("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")))
    if chemin_fichier_selectionne:
        extension = obtenir_extension_fichier(chemin_fichier_selectionne)
        messagebox.showinfo("Extension du fichier", f"L'extension du fichier est : {extension}")

def convertir_csv():
    if chemin_fichier_selectionne:
        chemin_fichier_sortie = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")))
        if chemin_fichier_sortie:
            convertir_en_csv(chemin_fichier_selectionne, chemin_fichier_sortie, delimiteur='\t')  # Convertir en CSV avec un délimiteur de tabulation
            messagebox.showinfo("Conversion en CSV", f"Le fichier a été converti en CSV avec succès. Chemin du fichier : {chemin_fichier_sortie}")
    else:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez d'abord sélectionner un fichier à convertir.")

def convertir_json():
    if chemin_fichier_selectionne:
        chemin_fichier_sortie = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")))
        if chemin_fichier_sortie:
            convertir_en_json(chemin_fichier_selectionne, chemin_fichier_sortie)
            messagebox.showinfo("Conversion en JSON", f"Le fichier a été converti en JSON avec succès. Chemin du fichier : {chemin_fichier_sortie}")
    else:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez d'abord sélectionner un fichier à convertir.")

def convertir_yaml():
    if chemin_fichier_selectionne:
        chemin_fichier_sortie = filedialog.asksaveasfilename(defaultextension=".yaml", filetypes=(("Fichiers YAML", "*.yaml"), ("Tous les fichiers", "*.*")))
        if chemin_fichier_sortie:
            convertir_en_yaml(chemin_fichier_selectionne, chemin_fichier_sortie)
            messagebox.showinfo("Conversion en YAML", f"Le fichier a été converti en YAML avec succès. Chemin du fichier : {chemin_fichier_sortie}")
    else:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez d'abord sélectionner un fichier à convertir.")

def convertir_xml():
    if chemin_fichier_selectionne:
        chemin_fichier_sortie = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=(("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")))
        if chemin_fichier_sortie:
            convertir_en_xml(chemin_fichier_selectionne, chemin_fichier_sortie)
            messagebox.showinfo("Conversion en XML", f"Le fichier a été converti en XML avec succès. Chemin du fichier : {chemin_fichier_sortie}")
    else:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez d'abord sélectionner un fichier à convertir.")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry('700x500')
fenetre.title('Ordinateur Routier - Afficher Extension de Fichier')
fenetre['bg'] = 'blue'
fenetre.resizable(height=False, width=False)

# Ajouter un bouton pour déclencher la sélection d'un fichier et afficher son extension
bouton_afficher = tk.Button(fenetre, text="Sélectionner un Fichier et Afficher Extension", command=afficher_extension, font=('verdana', 14), bg='skyblue', fg='white', padx=20, pady=10)
bouton_afficher.pack(pady=20)

# Ajouter un bouton pour déclencher la conversion en CSV
bouton_csv = tk.Button(fenetre, text="Convertir en CSV", command=convertir_csv, font=('verdana', 14), bg='green', fg='white', padx=20, pady=10)
bouton_csv.pack(pady=20)

# Ajouter un bouton pour déclencher la conversion en JSON
bouton_json = tk.Button(fenetre, text="Convertir en JSON", command=convertir_json, font=('verdana', 14), bg='orange', fg='white', padx=20, pady=10)
bouton_json.pack(pady=20)

# Ajouter un bouton pour déclencher la conversion en YAML
bouton_yaml = tk.Button(fenetre, text="Convertir en YAML", command=convertir_yaml, font=('verdana', 14), bg='purple', fg='white', padx=20, pady=10)
bouton_yaml.pack(pady=20)

# Ajouter un bouton pour déclencher la conversion en XML
bouton_xml = tk.Button(fenetre, text="Convertir en XML", command=convertir_xml, font=('verdana', 14), bg='red', fg='white', padx=20, pady=10)
bouton_xml.pack(pady=20)

chemin_fichier_selectionne = None

fenetre.mainloop()
