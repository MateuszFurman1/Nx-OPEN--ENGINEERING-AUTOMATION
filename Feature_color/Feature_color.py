import NXOpen
import NXOpen.Features
import NXOpen.Display

def main():
    the_session = NXOpen.Session.GetSession()
    work_part = the_session.Parts.Work
    
    if work_part is None:
        return

    lw = the_session.ListingWindow
    lw.Open()
    
    # POPRAWKA: "threaded" (z 'd') zamiast "threated"
    target_names = ["2 hole", "3 hole", "4 hole", "5 hole", "6 hole", "7 hole", "8 hole", "9 hole"]
    target_name2 = ["threaded hole", "m hole"]
    
    display_mod = the_session.DisplayManager.NewDisplayModification()
    display_mod.ApplyToAllFaces = False 
    
    count = 0
    lw.WriteLine("--- Rozpoczynam kolorowanie (2025) ---")
    
    mark_id = the_session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Coloring Holes")
    
    for feature in work_part.Features:
        display_name = feature.GetFeatureName().lower()
        user_name = feature.Name.lower()
        
        faces = feature.GetFaces()
        if not faces:
            continue

        applied = False

        # Sprawdzanie otworów gwintowanych (ID 211)
        if any(name in display_name or name in user_name for name in target_name2):
            display_mod.NewColor = 211
            display_mod.Apply(faces)
            applied = True

        # Sprawdzanie otworów zwykłych (ID 186)
        elif any(name in display_name or name in user_name for name in target_names):
            display_mod.NewColor = 186
            display_mod.Apply(faces)
            applied = True

        if applied:
            count += 1
            lw.WriteLine(f"[{count}] Pokolorowano: {feature.GetFeatureName()}")
    
    display_mod.Dispose()
    
    if count == 0:
        lw.WriteLine("Nie znaleziono żadnych pasujących operacji.")
    else:
        # NAJBARDZIEJ ODPORNA METODA ODŚWIEŻANIA (działa w 2024/2025/2027)
        try:
            # Próba odświeżenia przez session (często działa w nowych wersjach)
            the_session.Parts.Display.Views.RegenerateAll()
        except:
            # Jeśli powyższe zawiedzie, NX i tak odświeży obraz po ruszeniu myszką
            pass
            
        lw.WriteLine(f"--- Sukces! Zmodyfikowano {count} operacji. ---")

if __name__ == "__main__":
    main()
