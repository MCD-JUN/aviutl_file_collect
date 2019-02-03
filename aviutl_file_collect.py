### 実現したこと
### ・別ディレクトリ同一ファイル名の素材の処理
### 　・完全同一のファイルでもとりあえずファイル名に末尾を加えてコピーするようにしておく

### まだ実現していないこと
### ・フォントの取得（コピーもするかも）
### ・アニメーション効果の取得（環境によって差異があるため）
### ・カスタムオブジェクトの取得（理由は上記）
### ・githubにアップロード（公開したいね）

### 備忘録（exoファイルの仕様）
### ・イコール（=）の両端に半角スペースがあると読み込めない（スペース不要）
### ・要素名には大文字小文字の区別がある（X, Y, Zをx, y, zにすると座標情報が読み込まれない）
### ・ヘッダの前に空行があるのは問題ない（これは意外）
### ・シーン読み込みを利用すると「=1」という謎の行が存在するようになる。これがあるとConfigparserでの読み込みができない
### 　・Configparserでの読み込み前に「=1」を「hoge=1」のような感じに変更して、処理後に「=1」に戻すことにより解決

import os
import configparser
import sys
import shutil

debug = 0
linelength = 70

class Debug:
    def __init__(self, debug):
        if debug >= 1: self.flag = 1

    def filelist(self, files):
        if self.flag >= 1:
            print("[デバッグ]現在のfilesの内容")
            [print(i, name) for i, name in enumerate(files, 1)]
            os.system("pause")
            print()

class Filesearch:
    def __init__(self):
        self.dir = os.getcwd()

    def search(self):
        if len(sys.argv) >= 2:
            self.findfile = [f for i, f in enumerate(sys.argv) if i > 0]
        else:
            self.findfile = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f)) and f.rsplit(".", 1)[1] == "exo"]
        return self.findfile

class Path:
    def __init__(self, path, count, filescount):
        try:
            self.f_path = path
        except IndexError:
            print("エラー：exoファイルが指定されていません")
            os.system("pause")
            sys.exit("ExoFileNotRead")
        else:
            print("[%d/%d]読み込まれたファイル：%s" % (count, filescount, self.f_path))
        finally:
            print("-" * linelength)

    def show(self):
        print("path: %s" % self.f_path)
        os.system("pause")

    def check(self):
        result = os.path.isfile(self.f_path)
        if debug >= 1:
            print("\n[デバッグ]指定されたexoファイルの存在：%s" % result)
            os.system("pause")
            print()
        if result == False:
            print("\nエラー：指定されたexoファイルは存在しません")
            sys.exit("ExoFileNotFound")
        return self.f_path

class Exo:
    def __init__(self, exo_path):
        self.exo_path = exo_path
        self.writeflag = 0
        while True:
            try:
                self.exo = configparser.ConfigParser()
                self.exo.optionxform = str
                self.exo.read(exo_path)
            except configparser.ParsingError:
                edit = Edit(exo_path)
                sf_name = edit.makedir()
                del edit

                src = os.path.abspath(exo_path)
                dst = sf_name[0] + "\\" + (os.path.basename(os.path.abspath(exo_path))).rsplit(".", 1)[0] + "_old2.exo"
                shutil.copy2(src, dst)

                with open(exo_path) as self.f:
                    self.f = self.f.readlines()

                self.f2 = []
                for f in self.f:
                    f2 = "configparsererroravoidance=1\n" if f == "=1\n" else f
                    self.f2.append(f2)

                with open(src, "w") as fr:
                    fr.writelines(self.f2)

                self.writeflag = 1
            else:
                break
    
    def __del__(self):
        if self.writeflag == 1:
            with open(self.exo_path) as self.f:
                self.f = self.f.readlines()
            self.f2 = []
            for f in self.f:
                f2 = "=1\n" if f == "configparsererroravoidance=1\n" else f
                self.f2.append(f2)
            with open(self.exo_path, "w") as fr:
                fr.writelines(self.f2)

    def check(self):
        print("素材のファイルパスの取得中 . . .")
        exo = self.exo
        errorcount = 0
        self.files2 = []
        for i, name in enumerate(exo.sections()):
            try:
                self.files2.append([exo.sections()[i], exo[name]["_name"], exo[name]["file"]])
            except KeyError:
                pass
        
        self.files = [f for f in self.files2 if f[1] in ["動画ファイル", "画像ファイル", "音声ファイル"]]

        self.copydict_src = []
        self.copydict_src3 = []
       
        self.copydict_src = [f for f in [f[2] for f in self.files] if f not in self.copydict_src and not self.copydict_src.append(f)]
        self.copydict_src2 = [[i, f.rsplit("\\", 1)[0], f.rsplit("\\", 1)[1]] for i, f in enumerate(self.copydict_src)]
        
        for i, name in enumerate(self.copydict_src2):
            self.copydict_src3.append([name[1], name[2], name[1], name[2]])
            for name2 in self.copydict_src3:
                if name[1] != name2[0] and name[2] == name2[1]:
                    j = 0
                    for name3 in self.copydict_src3:
                        if name[2] == name3[1]:
                            j += 1
                    self.copydict_src3[i][3] = name[2].rsplit(".",1)[0] + "_" + str(j) + "." + name[2].rsplit(".",1)[1]

        self.files2 = [[f[0] + "\\" + f[1], f[2] + "\\" + f[3]] for f in self.copydict_src3]
        
        self.files3 = []

        for f in self.files:
            for f2 in self.files2:
                if f[2] == f2[0]:
                    if f2[0] == f2[1]:
                        self.files3.append([f[0], f[1], f[2]])
                    else:
                        self.files3.append([f[0], f[1], f2[1]])

        print("\n完了\n" + "-" * linelength)
        
        if len(self.files) == 0:
            print("エラー：外部参照されているファイルが存在しません")
            sys.exit("ExternalFileNotFound")
        
        if debug >= 1:
            print("[デバッグ]現在のfilesの内容")
            [print(i, name) for i, name in enumerate(self.files, 1)]
            os.system("pause")
            print()

        print("元ファイルの存在を確認中 . . .")

        for i, name in enumerate(self.files):
            result = os.path.isfile(name[2])
            (self.files[i]).append(result)
            if result == False:
                if errorcount == 0: print("\n下記のファイルが見つかりません")
                print(name[2])
                errorcount += 1

        if errorcount > 0:
            print("\n警告：%d個のファイルが見つかりませんでした" % errorcount)
            while True:
                result = input("続行しますか？(Y/N)：")
                if result in ["y", "Y", "yes", "Yes", "YES"]:
                    print("\n続行します\n")
                    break
                elif result in ["n", "N", "no", "No", "NO"]:
                    print("\n中止します")
                    sys.exit("ExternalFileNotFound")
                else:
                    print("\nエラー：入力値が不正です\n")

        print("\n完了\n\n検出ファイル数：" + str(len(self.files)) + "\n" + "-" * linelength)

        if debug >= 1:
            print("[デバッグ]現在のfilesの内容")
            [print(i, name) for i, name in enumerate(self.files, 1)]
            os.system("pause")
            print()

        return self.files, self.files3

class Edit:
    def __init__(self, f_path):
        self.f_path = f_path

    def makedir(self):
        self.exo_abspath = os.path.abspath(self.f_path)
        self.basedir = os.path.dirname(self.exo_abspath)
        self.basename = (os.path.basename(self.exo_abspath)).rsplit(".", 1)
        self.dirname = self.basedir + "\\" + self.basename[0] + "_src"
        self.subfoldername = [self.dirname + "\\" + name for name in ["old", "sound", "picture", "movie"]]
        try:
            os.mkdir(self.dirname)
            [os.mkdir(name) for name in self.subfoldername]
        except FileExistsError:
            pass
        finally:
            return self.subfoldername
            
    def filecopy(self, files, files2):
        self.files = files
        self.files2 = files2
        print("素材ファイルのコピー中 . . .")
        shutil.copy2(self.exo_abspath, self.dirname + "\\old\\" + self.basename[0] + "_old." + self.basename[1])
        copyfilecount, samefilecount = 0, 0
        for i, name in enumerate(self.files):
            try:
                file_src = name[2]
                file_src2 = self.files2[i][2]
                if name[3] == False:
                    file_dst = ""
                elif name[1] == "音声ファイル":
                    file_dst = self.dirname + "\\sound\\" + os.path.basename(file_src2)
                    shutil.copy2(file_src, file_dst)
                    copyfilecount += 1
                elif name[1] == "画像ファイル":
                    file_dst = self.dirname + "\\picture\\" + os.path.basename(file_src2)
                    shutil.copy2(file_src, file_dst)
                    copyfilecount += 1
                elif name[1] == "音声ファイル":
                    file_dst = self.dirname + "\\sound\\" + os.path.basename(file_src2)
                    shutil.copy2(file_src, file_dst)
                    copyfilecount += 1
                else:
                    file_dst = ""
                (self.files[i]).append(file_dst)
            except shutil.SameFileError:
                samefilecount += 1
            
        print("\n情報：%d個のファイルをコピーしました" % copyfilecount)
        if samefilecount > 0:
            print("情報：%d個のファイルは既にコピーされていました" % samefilecount)
        
        if debug >= 1:
            print("\n[デバッグ]現在のfilesの内容")
            [print(i, name) for i, name in enumerate(self.files, 1)]
            os.system("pause")
            print()
        
        print("\n完了\n" + "-" * linelength)

    def fontcopy(self):
        pass

    def exoedit(self):
        print("exoファイルを編集中 . . .")
        try:
            exo = configparser.ConfigParser()
            exo.optionxform = str
            exo.read(self.exo_abspath)
            for name in self.files:
                exo[name[0]]["file"] = name[4]

            with open(self.exo_abspath, "w") as exofile:
                exo.write(exofile, space_around_delimiters = False)
        except IndexError:
            print("\n情報：exoファイルの編集は不要のため、編集はしていません")
        print("\n完了\n" + "-" * linelength)

def main():
    #dbg = Debug(1)

    print("AviUtl ファイルまとめツール\n")

    fs = Filesearch()
    files = fs.search()
    print("読み込まれたファイルの一覧")
    [print(f) for f in files]
    print()
    os.system("pause")
    print()

    filescount = len(files)

    for i, name in enumerate(files, 1):
        try:
            path = Path(name, i, filescount)
            f_path = path.check()
            exo = Exo(f_path)
            files, files2 = exo.check()
            edit = Edit(f_path)
            print("コピー先のフォルダを作成中 . . .")
            edit.makedir()
            print("\n完了\n" + "-" * linelength)
            edit.filecopy(files, files2)
            edit.exoedit()
        except SystemExit:
            if i < filescount: print("\n次のファイルに進みます")
            os.system("pause")
            print("-" * linelength)
        finally:
            del exo
    
    if filescount == 0: print("エラー：ファイルが指定されていません\n")
    print("すべての処理が完了しました")
    os.system("pause")

if __name__ == "__main__":
    main()