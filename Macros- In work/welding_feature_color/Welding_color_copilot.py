import NXOpen
import NXOpen.Features

def main():
    the_session = NXOpen.Session.GetSession()
    work_part = the_session.Parts.Work
    
    if work_part is None:
        return

    lw = the_session.ListingWindow
    lw.Open()
    
    count = 0
    target_color = 6  # Żółty
    
    lw.WriteLine("--- Próba kolorowania bezpośredniego (Face.Color) ---")
    
    # Rozpoczynamy Undo Mark, aby zmiany były widoczne i możliwe do cofnięcia
    mark_id = the_session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Coloring Holes")
    
    for feature in work_part.Features:
        display_name = feature.GetFeatureName()
        user_name = feature.Name
        
        if "hole" in display_name.lower() or "hole" in user_name.lower():
            faces = feature.GetFaces()
            
            if faces:
                count += 1
                lw.WriteLine(f"Przetwarzanie: {display_name} (Ścian: {len(faces)})")
                
                for face in faces:
                    # Bezpośrednia zmiana koloru każdej ściany z osobna
                    face.Color = target_color
                    # Wymuszenie odświeżenia wyglądu obiektu
                    face.RedisplayObject()

    # Odświeżenie widoku graficznego po zakończeniu pętli
    if count > 0:
        the_session.RegenerateAllViews()
        lw.WriteLine(f"--- Zakończono. Zmodyfikowano {count} operacji. ---")
    else:
        lw.WriteLine("Nie znaleziono operacji 'hole'.")

if __name__ == "__main__":
    main()
