using System;
using System.Collections.ObjectModel;
using System.Data.Common;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Newtonsoft.Json;
using Microsoft.WindowsAPICodePack.Dialogs;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Window;
using System.Text.RegularExpressions;
using System.Media;
using System.Security.Principal;
using System.Security.Cryptography;
using MCWiiU_Texture_Builder__Frontend;
using Path = System.IO.Path;
using System.Printing;

namespace MCWiiU_Texture_Builder___Frontend
{
    public partial class MainWindow : Window
    {
        // global variables to this class
        private List<string> InputGames = new List<string>();
        private List<string> InputVersionsJava = new List<string>();
        private List<string> InputVersionsBedrock = new List<string>();
        private List<string> OutputDrives = new List<string>();
        private List<string> BuildModes = new List<string>();
        private List<string> OutputGamesWiiu = new List<string>();
        private List<string> OutputGamesSwitch = new List<string>();
        private List<string> OutputGamesXB360 = new List<string>();
        private List<string> OutputGamesXBO = new List<string>();
        private List<string> OutputGamesPS3 = new List<string>();
        private List<string> OutputGamesPSV = new List<string>();
        private List<string> OutputGamesPS4 = new List<string>();
        private List<string> CurrentOutputGames = new List<string>();
        private List<string> SizeModes = new List<string>();
        private string DocumentsPath = System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\Texture_Builder\\";
        private bool DontSaveDefault = false;
        bool debugMode = false;

        // setup
        public MainWindow()
        { // initial setup
            InitializeComponent();

            // --- UI SETUP --- 

            DontSaveDefault = true;

            // InputGames
            InputGames = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\input_games.json");
            InputGameCombo = ArrayToCombo(InputGameCombo, InputGames);

            // versions
            InputVersionsJava = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\input_versions_java.json");
            InputVersionsBedrock = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\input_versions_bedrock.json");

            // location
            OutputDrives = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_drives.json");
            OutputDriveCombo = ArrayToCombo(OutputDriveCombo, OutputDrives);

            // oversized modes
            BuildModes = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\modes_build.json");
            BuildModeCombo = ArrayToCombo(BuildModeCombo, BuildModes);
            BuildModeCombo.SelectedIndex = 0;

            // write modes
            OutputGamesWiiu = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_wiiu.json");
            OutputGamesSwitch = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_nintendo_switch.json");
            OutputGamesXB360 = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_xbox360.json");
            OutputGamesXBO = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_xbox_one.json");
            OutputGamesPS3 = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_ps3.json");
            OutputGamesPSV = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_psv.json");
            OutputGamesPS4 = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\output_structures_ps4.json");
            setOutputGameComboOptions(["all"]);

            // size modes
            SizeModes = JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\modes_size.json");
            SizeModeCombo = ArrayToCombo(SizeModeCombo, SizeModes, "x", 2);
            SizeModeCombo.SelectedIndex = 0;

            // supported version
            SupportLabel.Text += " " + JsonReadFileAsStringList(Directory.GetCurrentDirectory() + "\\python_builder\\global\\supported_versions.json")[0] + "(0)";

            // apply the currently stored selections
            applySelections();
            DontSaveDefault = false;
        }

        // method to easily set output game options
        private void setOutputGameComboOptions(string[] pool)
        {
            var toAdd = new List<string>();
            foreach (string str in pool)
            {
                switch (str)
                {
                    case "wiiu":
                        toAdd = toAdd.Concat(OutputGamesWiiu).ToList();
                        break;
                    case "nintendo switch":
                        toAdd = toAdd.Concat(OutputGamesSwitch).ToList();
                        break;
                    case "xbox 360":
                        toAdd = toAdd.Concat(OutputGamesXB360).ToList();
                        break;
                    case "xbox one":
                        toAdd = toAdd.Concat(OutputGamesXBO).ToList();
                        break;
                    case "ps 3":
                        toAdd = toAdd.Concat(OutputGamesPS3).ToList();
                        break;
                    case "ps vita":
                        toAdd = toAdd.Concat(OutputGamesPSV).ToList();
                        break;
                    case "ps 4":
                        toAdd = toAdd.Concat(OutputGamesPS4).ToList();
                        break;
                    case "all":
                        toAdd = toAdd.Concat(OutputGamesWiiu)
                            .Concat(OutputGamesSwitch)
                            .Concat(OutputGamesXB360)
                            .Concat(OutputGamesXBO)
                            .Concat(OutputGamesPS3)
                            .Concat(OutputGamesPSV)
                            .Concat(OutputGamesPS4)
                            .ToList();
                        break;
                }
            }
            CurrentOutputGames = toAdd;
            OutputGameCombo.Items.Clear();
            OutputGameCombo = ArrayToCombo(OutputGameCombo, toAdd);
        }

        // function for determining what game the selection is part of
        private string getGame(string selection)
        {
            switch (selection)
            {
                case "java folder":
                case "java .zip file":
                    return "java";
                case "bedrock folder":
                case "bedrock .mcpack file":
                    return "bedrock";
                case "wiiu default textures":
                    return "wiiu";
                default:
                    return "";
            }
        }

        // function for determining what type of input the selection is
        private string getInputType(string selection)
        {
            switch (selection)
            {
                case "bedrock .mcpack file":
                    return ".mcpack";
                case "java .zip file":
                    return ".zip";
                case "bedrock folder":
                case "java folder":
                    return "folder";
                case "wiiu default textures":
                    return "none";
                default:
                    return "";
            }
        }

        // JSON //

        // selections class for the json object that is written
        private class Selections()
        {
            public string InputText = "";
            public string OutputText = "";
            public int gameIndex = -1;
            public int versionIndex = -1;
            public int locationIndex = -1;
            public int oversizedIndex = -1;
            public int writeIndex = -1;
            public int sizeIndex = -1;
            public int wiiuStoredOversizedIndex = -1;
        }

        private Selections selections = new Selections();

        // function for reading json as a string list
        private List<string> JsonReadFileAsStringList(string path)
        {
            return JsonConvert.DeserializeObject<List<string>>(File.ReadAllText(path));
        }
        // Function for reading json as a selections list
        private List<Selections> JsonReadFileAsSelectionsList(string path)
        {
            return JsonConvert.DeserializeObject<List<Selections>>(File.ReadAllText(path));
        }

        private void JsonWriteFileSelections()
        {
            string json = JsonConvert.SerializeObject(new List<Selections>() { selections });
            if (!Directory.Exists(DocumentsPath)) // make path if it doesn't exist
            { 
                Directory.CreateDirectory(DocumentsPath);
            }
            File.WriteAllText(DocumentsPath + "selections.json", json);
        }

        // when adding selections you must
            // add to Selections class
            // storeSelections
                // add default value check
                // add to selections
                // write file
            // applySelections
                // value possibility check
                // set the variable to what it's supposed to be
        
        // store selection function for storing user selections
        private void storeSelections() // writes the whole file each time to avoid having to make some weird naming scheme
        {
            if (DontSaveDefault) return;

            // set Selections variables (and check for default value)
            if (InputText != null) 
            { 
                if (!InputText.Text.Equals("Browse a path")) 
                { 
                    selections.InputText = InputText.Text;
                    JsonWriteFileSelections();
                } 
            }
            if (OutputText != null) 
            { 
                if (!OutputText.Text.Equals("Browse a path")) 
                { 
                    selections.OutputText = OutputText.Text;
                    JsonWriteFileSelections();
                } 
            }
            if (InputGameCombo != null) 
            { 
                if (!InputGameCombo.SelectedIndex.Equals(-1)) 
                { 
                    selections.gameIndex = InputGameCombo.SelectedIndex;
                    JsonWriteFileSelections();
                } 
            }
            if (InputVersionCombo != null)
            {
                if (!InputVersionCombo.SelectedIndex.Equals(-1))
                {
                    selections.versionIndex = InputVersionCombo.SelectedIndex;
                    JsonWriteFileSelections();
                }
            }
            if (OutputDriveCombo != null)
            {
                if (!OutputDriveCombo.SelectedIndex.Equals(-1))
                {
                    selections.locationIndex = OutputDriveCombo.SelectedIndex;
                    JsonWriteFileSelections();
                }
            }
            if (BuildModeCombo != null)
            {
                if (!BuildModeCombo.SelectedIndex.Equals(-1))
                {
                    selections.oversizedIndex = BuildModeCombo.SelectedIndex;
                    JsonWriteFileSelections();
                }
            }
            if (OutputGameCombo != null)
            {
                if (!OutputGameCombo.SelectedIndex.Equals(-1))
                {
                    selections.writeIndex = OutputGameCombo.SelectedIndex;
                    JsonWriteFileSelections();
                }
            }
            if (SizeModeCombo != null)
            {
                if (!SizeModeCombo.SelectedIndex.Equals(-1))
                {
                    selections.sizeIndex = SizeModeCombo.SelectedIndex;
                    JsonWriteFileSelections();
                }
            }
            // wiiu stored index is always written
        }

        // applies changed selections
        private void applySelections()
        {
            // read from file
            if (!File.Exists(DocumentsPath + "selections.json")) return; // if file doesn't exist then don't set stuff
            selections = JsonReadFileAsSelectionsList(DocumentsPath + "selections.json").ElementAt(0);

            // set variables from selection to respective places (will need to run checks on if you even can)
            //  the order these are set in matters
            if (selections.gameIndex != -1)
            {
                InputGameCombo.SelectedIndex = selections.gameIndex;
            }
            if (selections.InputText != "") 
            { 
                InputText.Text = selections.InputText; 
            }
            if (selections.OutputText != "") 
            { 
                OutputText.Text = selections.OutputText; 
            }
            if (selections.versionIndex != -1)
            {
                InputVersionCombo.SelectedIndex = selections.versionIndex;
            }
            if (selections.locationIndex != -1)
            {
                OutputDriveCombo.SelectedIndex = selections.locationIndex;
            }
            if (selections.oversizedIndex != -1 && selections.wiiuStoredOversizedIndex == -1)
            {
                BuildModeCombo.SelectedIndex = selections.oversizedIndex;
            }
            if (selections.writeIndex != -1)
            {
                OutputGameCombo.SelectedIndex = selections.writeIndex;
            }
            if (selections.sizeIndex != -1)
            {
                SizeModeCombo.SelectedIndex = selections.sizeIndex;
            }
        }

        // function for updating combo box items
        private System.Windows.Controls.ComboBox ArrayToCombo(System.Windows.Controls.ComboBox combo, List<string> arr, string addition="", int position=-1)
        {
            foreach (String item in arr)
            {
                string name = Char.ToUpper(item[0]) + item.Substring(1);
                int appensionPosition = (position == -1) ? name.Length : position;
                name = name.Insert(appensionPosition, addition);
                combo.Items.Add(name); // add and capitalize
            }
            return combo;
        }

        private void changeSelections(Action selectionsChangeFunction)
        {
            if (DontSaveDefault) return;
            selectionsChangeFunction();
        }

        private bool wiiuNeedsToBeEnabled = false;
        
        // function to disable ui for wiiu defaults
        private void disableWiiu()
        {
            InputText.Text = "Browse a Path";
            changeSelections(() =>
            {
                selections.wiiuStoredOversizedIndex = BuildModeCombo.SelectedIndex; // stores index to go back to
            });
            BuildModeCombo.SelectedIndex = -1;

            InputButton.IsEnabled = false;
            InputVersionCombo.IsEnabled = false;
            BuildModeCombo.IsEnabled = false;

            wiiuNeedsToBeEnabled = true;
        }

        private void enableWiiu()
        {
            if (wiiuNeedsToBeEnabled == false) return;
            wiiuNeedsToBeEnabled = false;

            BuildModeCombo.SelectedIndex = selections.wiiuStoredOversizedIndex;
            changeSelections(() =>
            {
                selections.wiiuStoredOversizedIndex = -1;
            });

            InputButton.IsEnabled = true;
            InputVersionCombo.IsEnabled = true;
            BuildModeCombo.IsEnabled = true;
        }
        
        // InputGameCombo selection changed
        private void InputGameCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // function to re-enable ui for non-wiiu defaults

            InputText.Text = "Browse a Path"; // clear input text when game changes
            InputVersionCombo.Items.Clear();
            var combo = InputVersionCombo;
            if (getGame(InputGames[InputGameCombo.SelectedIndex]) == "java")
            {
                combo = ArrayToCombo(InputVersionCombo, InputVersionsJava, "+");
                setOutputGameComboOptions(["all"]);
                enableWiiu();
            }
            else if (getGame(InputGames[InputGameCombo.SelectedIndex]) == "bedrock")
            {
                combo = ArrayToCombo(InputVersionCombo, InputVersionsBedrock, "+");
                setOutputGameComboOptions(["all"]);
                enableWiiu();
            } else
            {
                // else is an empty combo, so we dont have to set it, just change other properties
                var toSelect = new List<string>();
                switch (InputGameCombo.SelectedIndex)
                {
                    case 4:
                        toSelect.Add("xbox one");
                        toSelect.Add("nintendo switch");
                        break;
                    case 5:
                        toSelect.Add("wiiu");
                        break;
                    case 6:
                        toSelect.Add("xbox 360");
                        toSelect.Add("ps 3");
                        toSelect.Add("ps v");
                        break;
                    case 7:
                        toSelect.Add("ps 4");
                        break;
                }
                setOutputGameComboOptions(toSelect.ToArray());
                disableWiiu();
            }

            OutputGameCombo.SelectedIndex = 0;
            InputVersionCombo = combo;
            storeSelections();
        }

        // INFOBUTTON clicked
        private void BuildHelpButton_Click(object sender, RoutedEventArgs e)
        {
            Info info = new Info();
            info.ShowDialog();
        }

        // HELPBUTTON clicked
        private void ContactButton_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.MessageBox.Show(string.Join("\n", new string[] {
                "--- Having Trouble? Need Help? ---",
                "",
                "Contacts:",
                "- Discord Username: xLevia",
                "- Discord Server: https://discord.gg/bKD9FV63HA",
                "- Email: NightDrago9893@gmail.com",
                }), "Help");
        }

        // INPUTBUTTON clicked
        private void InputButton_Click(object sender, RoutedEventArgs e)
        {
            // checks for selected game
            if (InputGameCombo.SelectedIndex == -1) // no game
            {
                System.Windows.MessageBox.Show("Please select a game before browsing for input files!", "Error");
                return;
            } else if (getInputType(InputGames[InputGameCombo.SelectedIndex]) == "folder") // folder
            {
                // create folder dialog
                CommonOpenFileDialog folderDialog = new CommonOpenFileDialog();
                folderDialog.Title = "Select an input folder";
                folderDialog.IsFolderPicker = true;

                if (folderDialog.ShowDialog() == CommonFileDialogResult.Ok)
                {
                    InputText.Text = folderDialog.FileName;
                }
            } 
            else // file
            {
                // create file dialog
                CommonOpenFileDialog fileDialog = new CommonOpenFileDialog();
                fileDialog.Title = "Select an input file";
                string fileType = getInputType(InputGames[InputGameCombo.SelectedIndex]);
                fileDialog.Filters.Add(new CommonFileDialogFilter(fileType + " File", fileType));
                fileDialog.Filters.Add(new CommonFileDialogFilter(".jar File", ".jar"));

                if (fileDialog.ShowDialog() == CommonFileDialogResult.Ok)
                {
                    InputText.Text = fileDialog.FileName;
                }
            }
        }

        // OUTPUTBUTTON clicked
        private void OutputButton_Click(object sender, RoutedEventArgs e)
        {
            // create folder dialog
            CommonOpenFileDialog folderDialog = new CommonOpenFileDialog();
            folderDialog.Title = "Select an output folder";
            folderDialog.IsFolderPicker = true;

            if (folderDialog.ShowDialog() == CommonFileDialogResult.Ok)
            {
                OutputText.Text = folderDialog.FileName;
            }
        }

        // BUILDBUTTON clicked
        private void BuildButton_Click(object sender, RoutedEventArgs e)
        {
            // initial checks
            List<string> Errors = new List<string>();

            // check for errors
            if ((InputText.Text == null || InputText.Text == "Browse a Path") && getGame(InputGames[InputGameCombo.SelectedIndex]) != "wiiu")
            {
                Errors.Add("Input Path is not set");
            }
            if (!Path.Exists(InputText.Text) && InputText.Text != "Browse a Path")
            {
                Errors.Add($"Path doesn't exist: {InputText.Text}");
            }
            if (OutputText.Text == null || OutputText.Text == "Browse a Path")
            {
                Errors.Add("Output path is not set");
            }
            if (!Path.Exists(OutputText.Text) && OutputText.Text != "Browse a Path")
            {
                Errors.Add($"Path doesn't exist: {OutputText.Text}");
            }
            if (InputGameCombo.SelectedIndex == -1)
            {
                Errors.Add("No game is selected");
            }
            if (OutputGameCombo.SelectedIndex == -1)
            {
                Errors.Add("No output structure was selected");
            }
            if ((InputVersionCombo.SelectedIndex == -1) && getGame(InputGames[InputGameCombo.SelectedIndex]) != "wiiu")
            {
                Errors.Add("No version is selected");
            }
            if (!(CurrentOutputGames[OutputGameCombo.SelectedIndex].EndsWith("dump")
                || (CurrentOutputGames[OutputGameCombo.SelectedIndex] == "wiiu modpack (sdcafiine)")))
            {
                if (OutputDriveCombo.SelectedIndex == -1)
                {
                    Errors.Add("No location is selected");
                }
            }

            // display errors and return if they exist
            if (Errors.Count != 0)
            {
                System.Windows.MessageBox.Show(
                    "The following errors were encountered before trying to build textures:\n\n- " + string.Join("\n- ", Errors),
                    "Error");
                return;
            }

            // create
            var programEntry = new ProcessStartInfo();
            programEntry.FileName = Directory.GetCurrentDirectory() + "\\python_builder\\Entry_Program.exe";
            string version = "none";
            if (getGame(InputGames[InputGameCombo.SelectedIndex]) == "java")
            {
                version = InputVersionsJava.ToArray()[InputVersionCombo.SelectedIndex].Replace("+", "");
            } else if (getGame(InputGames[InputGameCombo.SelectedIndex]) == "bedrock")
            {
                version = InputVersionsBedrock.ToArray()[InputVersionCombo.SelectedIndex].Replace("+", "");
            } // else does nothing for version, it equals "none"

            const bool python_debug_mode = false;

            string[] inputArgs = 
            { 
                InputText.Text, // input path (1)
                OutputText.Text, // output path (2)
                getGame(InputGames[InputGameCombo.SelectedIndex]), // input game (3)
                getInputType(InputGames[InputGameCombo.SelectedIndex]), // input file/folder type (4)
                version, // input version (5)
                (getGame(InputGames[InputGameCombo.SelectedIndex]) != "wiiu") ? BuildModes[BuildModeCombo.SelectedIndex] : "null", // build or replace (6)
                CurrentOutputGames[OutputGameCombo.SelectedIndex], // output game (7)
                OutputDrives[OutputDriveCombo.SelectedIndex], // drive (8)
                "python_builder", // location of the python file (9)
                python_debug_mode.ToString(), // debug mode (10)
                Regex.Replace(SizeModes[SizeModeCombo.SelectedIndex], "[a-zA-Z ]", ""), // size (11)  
                (Regex.Replace(SizeModes[SizeModeCombo.SelectedIndex], "[0-9 ]", "") == "simpleprocessing") ? "False" : "True" // complex processing type (12)
            };

            programEntry.Arguments = "\"" + string.Join("\" \"", inputArgs); // join arguments

            // process configuration
            programEntry.UseShellExecute = false;
            programEntry.CreateNoWindow = true;
            programEntry.RedirectStandardOutput = true;
            programEntry.RedirectStandardError = true;

            // execute and get output
            var errors = "";
            var results = "";

            using (Process process = Process.Start(programEntry))
            {
                errors = process.StandardError.ReadToEnd(); // debug variable
                results = process.StandardOutput.ReadToEnd();
            }

            // handle output (errors are not printed, but they are collected)
            if (results != "") // if there's results
            {
                if (python_debug_mode == false)
                { // wont create a message box if debug is enabled (to avoid crashes)
                    Debug.Write(results);
                    System.Windows.MessageBox.Show("Build did NOT complete!\n" + results, "Error");
                }
            } else
            {
                System.Windows.MessageBox.Show("Success!\nThe build completed", "Complete");
            }

            // DEBUGGING ONLY
            if (debugMode == true)
            {
                if (errors != "")
                {
                    Debug.Write(errors);
                }
            }
        }

        // OPENBUTTON clicked
        private void OpenButton_Click(object sender, RoutedEventArgs e)
        {
            string OpenLocation = OutputText.Text;
            if (InputText.Text == null || InputText.Text == "Browse a Path")
            {
                OpenLocation = "C:\\Users\\" + WindowsIdentity.GetCurrent() + "\\documents";
            }
            Process.Start("explorer.exe", OpenLocation);
        }

        private void InputText_TextChanged(object sender, TextChangedEventArgs e)
        {
            storeSelections();
        }

        private void OutputText_TextChanged(object sender, TextChangedEventArgs e)
        {
            storeSelections();
        }

        private void InputVersionCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            storeSelections();
        }

        private void OutputDriveCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            storeSelections();
        }

        private void BuildModeCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            storeSelections();
        }

        private void OutputGameCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if ((OutputGameCombo.SelectedIndex < CurrentOutputGames.Count) && (OutputGameCombo.SelectedIndex != -1))
            {
                // if dump or modpack
                if (CurrentOutputGames[OutputGameCombo.SelectedIndex].EndsWith("dump")
                    || (CurrentOutputGames[OutputGameCombo.SelectedIndex] == "wiiu modpack (sdcafiine)"))
                { // disable
                    OutputDriveCombo.IsEnabled = false;
                    OutputDriveCombo.SelectedIndex = 0; // set drive
                }
                else // not
                { // enable
                    OutputDriveCombo.IsEnabled = true;
                }
            } else
            { // enable
                OutputDriveCombo.IsEnabled = true;
            }
            storeSelections();
        }

        private void SizeModeCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if ((SizeModeCombo.SelectedIndex > 0) && (DontSaveDefault == false))
            {
                string warning = "Using texture packs larger than x16 may cause in-game performance to drop.";

                // simple processing
                if (Regex.Replace(SizeModes[SizeModeCombo.SelectedIndex], "[0-9 ]", "") == "simpleprocessing")
                {
                    warning += "\nSome sizes only allow simple processing to be used.";
                } else
                { // complex processing
                    warning += "\nAdditionally, using \"simple processing\" is recommended for packs bigger than x16.";
                }
    
                warning += "\nYou can find more info about size processing types in \"Help Configuring?\"";

                System.Windows.MessageBox.Show(warning, "Warning");
            }
            storeSelections();
        }
    }
}