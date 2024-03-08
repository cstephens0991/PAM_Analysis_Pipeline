# PAM_Analysis_Pipeline
Series of packages for the automation of PAM analysis from 24- or 48-well plates, using images generated by ImagingWin software.

The PAM analysis pipeline automates the extraction of plant photosynthetic area and photosynthetic efficiency (FvFm or Y(II)) data. These scripts, specifically for obtaining FvFm values of plants, was based on scripts previously published by Schneider et al., 2019 (https://doi.org/10.1186/s13007-019-0546-1) and released by the Donald Danforth Plant Science Center (https://plantcv.danforthcenter.org/). Thanks also to Walz GmbH (creator of ImaginWin software) for providing the pim2tiff executable for conversion of .xpim image files to tiff stacks.

## Setting up the environment and downloading the package
This step *only has to be carried out the first time you follow this protocol*. For repeat use of the pipeline, skip to ~~Part 2~~.

1\. Install Git. Go to https://git-scm.com/downloads and click the link for your operating system (e.g. Windows). Select the hyperlink at "Click here to download the latest...", to get the most up to date version. Select the recommended settings for the installation.

2\. Once installed, open Git bash (use the Windows search bar to find the program). This is the terminal for Git and should look similar to a regular Terminal/Command Prompt (see Figure 3). Now install "micromamba" (an "environment manager" program) by entering the following command:

```bash
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```

- Note: you can check that micromamba is correctly installed by printing the micromamba help window using the `micromamba -h` command. 
- Note: Important commands for navigating in Git bash include "`pwd`" (provide working directory; the path to where you are currently located), "`dir`" (print the contents of your current location) and "`cd`" (change directory). To go "up" in the path from your current location, use "`cd ..`".

3\. Clone the PAM_analysis_pipeline repository from GitHub to your computer (this contains the scripts for the pipeline).

- Note: The script will run faster if you clone the repository to your local computer and run it there, rather than your own folder in the sofs drive.
- First, navigate in `git bash` to the location where you want to clone the repository (a new folder will be created called "PAM_analysis_pipeline"). For example, if you want to create that directory inside your "Documents/" folder, you can run this command:

```bash
cd $HOME/Documents/
## to check what is present inside your Documents folder, use the ls command
ls
ls -lrth # these added options will list the contents in anti-chronological order, with some other information
```
**NB**: `cd` stands for **c**hange **d**irectory, so it's a command to navigate between folders inside the command line. 

To clone the repository, simply run the following command in `git bash`:
```bash
git clone https://github.com/cstephens0991/PAM_Analysis_Pipeline
## check it was added:
ls -lrth 
# should list at the bottom, the PAM_Analysis_Pipeline folder
## move into that folder:
cd PAM_Analysis_Pipeline
```

Other commands which may be useful in navigating to your required directory include:

- `dir`: returns a list of all files and folders in your current directory
- `pwd`: returns the path to you current location
- `cd ..`: move up one level in the path (into the parent directory)

- Your current path location is also printed in yellow immediately above the command line. ```~``` (tilde) represents your home directory. You can check which directory this is using `echo $HOME`.

- When writing directory or file names, pressing ```Tab``` can auto complete the name of the folder/file. If several files share the prefix already typed, pressing ```Tab``` twice, will print the available options:

![Figure 5: Use ```Tab``` to autocomplete directory/file names. Typing (for example) ```ls get_fvfm``` followed by pressing ```Tab``` twice returns the possible options (in the red box).](./screenshots/screenshot_17.jpg)

4\. Next, in Git bash create a new python environment in which to run the "PAM_analysis_packages" scripts. The following command will generate an environment called "get_fvfm" based on the specifications in the `get_fvfm_env.yml` file:

```bash
micromamba create -n get_fvfm --file PAM_analysis_packages/scripts/get_fvfm_env.yml
```

- Note: You can check which environments you have available using the command `micromamba env list` in Git bash.

5\. To edit the new "get_fvfm" environment we must first activate it:

```
micromamba activate get_fvfm
```

![*Figure 3:* Gitbash looks very similar to regular Command Prompt for Windows. One difference is it runs within an environment. The default environment is known as 'base'.](./screenshots/Screenshot_15.jpg)

6\. Finally, one more package should be installed, in order to parse arguments (options) for the main script. Unfortunately, this package is not available in micromamba, but is easily installed using `pip`. First check if `pip` is already installed (I think it should be on Git bash):

```bash
pip
```

If this does not give you something like "command not found", and instead returns a whole bunch of options, you're good to go. Otherwise, install `pip` by following the instructions on https://pip.pypa.io/en/stable/installation/. 

Then, run the following command, to install the package called `argparse`:

```bash
pip install argparse
```

After this, you are ready to follow the protocol in `markdown/pam_analysis_instructions.md`. 