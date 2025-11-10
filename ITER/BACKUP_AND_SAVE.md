# 💾 ITER - Kaip Išsaugoti Darbą / How to Save Your Work

## ✅ Kas Jau Išsaugota / What's Already Saved

Visi failai jau sukurti ir išsaugoti `C:\DI_MOKSLAI\ITER\` kataloge:

### Svarbiausi Failai / Key Files:
- ✅ Duomenų bazė: `database/iter.db` (7,936 procesai)
- ✅ Backend kodas: `backend/app/` (visi modeliai, servisai)
- ✅ Streamlit UI: `streamlit_app/` (visos puslapiai)
- ✅ Skriptai: `scripts/` (importavimas, setup)
- ✅ Dokumentacija: visi .md failai

### Viso Sukurta / Total Created:
- 📁 **40+ Python failų**
- 📊 **Duomenų bazė su 7,936 įrašais**
- 📚 **10+ dokumentacijos failų**
- 🎨 **5 Streamlit puslapiai**

---

## 🔐 Kaip Išsaugoti Saugiai / How to Backup Safely

### Variantas 1: Git (Rekomenduojama / Recommended)

```bash
cd C:\DI_MOKSLAI\ITER

# Inicializuoti Git
git init

# Pridėti visus failus
git add .

# Commit
git commit -m "ITER v1.0 - Complete hierarchical requirements discovery system"
```

### Variantas 2: ZIP Archyvas / ZIP Archive

```bash
# Sukurti ZIP
Compress-Archive -Path "C:\DI_MOKSLAI\ITER" -DestinationPath "C:\DI_MOKSLAI\ITER_BACKUP_$(Get-Date -Format 'yyyy-MM-dd').zip"
```

### Variantas 3: Nukopijuoti / Copy to Another Location

```bash
# Kopijuoti į kitą vietą
Copy-Item -Path "C:\DI_MOKSLAI\ITER" -Destination "D:\Backups\ITER_$(Get-Date -Format 'yyyy-MM-dd')" -Recurse
```

---

## 📦 Kas Turi Būti Išsaugota / What Should Be Saved

### ✅ Būtina / Essential:
- `backend/` - Visas backend kodas
- `streamlit_app/` - Visas UI kodas
- `scripts/` - Visi skriptai
- `database/iter.db` - Duomenų bazė (SVARBU!)
- `requirements.txt` - Python priklausomybės
- Visi `.md` failai - Dokumentacija

### ⚠️ Galima Praleisti / Can Skip:
- `__pycache__/` - Python cache
- `.pyc` failai - Compiled Python

---

## 🚀 Kaip Atkurti Projektą Kitame Kompiuteryje / How to Restore on Another PC

### 1. Nukopijuoti ITER katalogą
```bash
# Nukopijuoti visą ITER katalogą į naują kompiuterį
```

### 2. Įdiegti Python priklausomybes
```bash
cd ITER
pip install -r requirements.txt
```

### 3. Paleisti Streamlit
```bash
cd streamlit_app
streamlit run app.py
```

**Viskas veiks iš karto!** Duomenų bazė jau turi visus 7,936 procesus.

---

## 📝 Greitasis Išsaugojimas / Quick Save

Dabar sukursiu Git commit jums:















