"""
Réorganise le dataset SH17 (dossier archive/) en trois splits disjoints.

Structure source (archive/) :
  images/           <- 8099 images à plat
  labels/           <- 8099 .txt YOLO à plat
  train_files.txt   <- 6479 noms de fichiers
  val_files.txt     <- 1620 noms de fichiers

Structure cible (SH17dataset/) :
  images/train/  images/val/  images/test/
  labels/train/  labels/val/  labels/test/
  sh17.yaml

Splits : train=6479  val=1458  test=162  (test = 10% du val original, retiré du val)
"""

import shutil
import random
from pathlib import Path

SRC  = Path(r"C:\Users\luigi\OneDrive\Documents\Ecole 18.06\Traitement_image\Projet\archive")
DST  = Path(r"C:\Users\luigi\OneDrive\Documents\Ecole 18.06\Traitement_image\Projet\SH17dataset")

TEST_RATIO = 0.10   # 10 % du val → test


def read_split(txt: Path) -> list[str]:
    return [l.strip() for l in txt.read_text().splitlines() if l.strip()]


def copy_split(file_names: list[str], split: str):
    img_dst = DST / "images" / split
    lbl_dst = DST / "labels" / split
    img_dst.mkdir(parents=True, exist_ok=True)
    lbl_dst.mkdir(parents=True, exist_ok=True)

    ok, missing = 0, []
    for name in file_names:
        stem   = Path(name).stem
        img_src = SRC / "images" / name
        lbl_src = SRC / "labels" / (stem + ".txt")

        if not img_src.exists():
            missing.append(name)
            continue

        shutil.copy2(img_src, img_dst / name)
        if lbl_src.exists():
            shutil.copy2(lbl_src, lbl_dst / (stem + ".txt"))
        ok += 1

    print(f"  [{split:5s}]  {ok} fichiers copiés", end="")
    if missing:
        print(f"  ⚠ {len(missing)} images manquantes", end="")
    print()


def write_yaml():
    yaml = f"""path: {DST.as_posix()}
train: images/train
val:   images/val
test:  images/test

names:
  0:  person
  1:  ear
  2:  ear-mufs
  3:  face
  4:  face-guard
  5:  face-mask
  6:  foot
  7:  tool
  8:  glasses
  9:  gloves
  10: helmet
  11: hands
  12: head
  13: medical-suit
  14: shoes
  15: safety-suit
  16: safety-vest
"""
    (DST / "sh17.yaml").write_text(yaml)
    print(f"  sh17.yaml : {DST / 'sh17.yaml'}")


def main():
    for p in [SRC / "images", SRC / "labels", SRC / "train_files.txt", SRC / "val_files.txt"]:
        if not p.exists():
            print(f"ERREUR : introuvable → {p}"); return

    train = read_split(SRC / "train_files.txt")
    val   = read_split(SRC / "val_files.txt")

    random.seed(42)
    n_test   = max(1, int(len(val) * TEST_RATIO))
    test     = random.sample(val, n_test)
    test_set = set(test)
    val_only = [f for f in val if f not in test_set]

    print(f"Splits : train={len(train)}  val={len(val_only)}  test={len(test)}\n")

    copy_split(train,    "train")
    copy_split(val_only, "val")
    copy_split(test,     "test")

    write_yaml()
    print("\nTerminé.")


if __name__ == "__main__":
    main()
