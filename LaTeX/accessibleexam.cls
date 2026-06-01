%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%                                                                    %%%%%
%%%%% Version 1: Accessible LaTeX Exam Class                             %%%%%
%%%%% Not as feature rich as the original Exam Class, but a              %%%%%
%%%%% reasonable start. Sample exam is PDF/UA Compliant.                 %%%%%
%%%%% Author: Kris Hollingsworth, PhD                                    %%%%%
%%%%% Original Date: 4/25/2026                                           %%%%%
%%%%%                                                                    %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{accessibleexam}[Accessible Exam Class Version 1]

% ********* Start with article class defaults *********
\LoadClass[12pt]{article}

% ********* Page Geometry *********
\RequirePackage{geometry}
\geometry{
  left=.75in, right=.75in,
  top=.8in, bottom=1in,
  headheight=14.5pt,
  headsep=0.15in}

% ********* Some formatting choices *********
\makeatletter
\renewcommand{\section}{\@startsection
  {section}{1}{0mm}                % name, level, indent
  {0ex}% beforeskip (negative = no indent for next para)
  {1.3ex \@plus.2ex}                % afterskip
  {\centering\normalfont\Large\bfseries}}     % style
\makeatother
\setlength{\parindent}{0pt}

% ********* Helps with new document commands *********
\RequirePackage{xparse}

% ********* Planned future expansion *********
\newif\ifsolutions
\DeclareOption{solutions}{\solutionstrue}
\DeclareOption{nosolutions}{\solutionsfalse}
\ExecuteOptions{nosolutions}
\ProcessOptions\relax

% ********* Let's load a few packages *********
\RequirePackage{amsmath, amssymb} %% Needs to be loaded before unicode-math.
\everymath{\displaystyle} %% Don't use small inline math. Can use \textstyle to override.
\RequirePackage{multicol,fancyhdr,lastpage} %% Required for Header/Footer and Cover Page.

\RequirePackage{iftex}
\ifLuaTeX
  \RequirePackage{unicode-math} %% Helps with MathML Generation.
\fi


% ********* Macros and commands to reset them. *********
\newcommand{\coursename}{}
\newcommand{\examtitle}{}
\newcommand{\examdate}{}
\newcommand{\instructions}{}

\newcommand{\course}[1]{\renewcommand{\coursename}{#1}}
\newcommand{\exam}[1]{\renewcommand{\examtitle}{#1}}
\newcommand{\examdateval}[1]{\renewcommand{\examdate}{#1}}
\newcommand{\setinstructions}[1]{\renewcommand{\instructions}{#1}}

% ********* Empty first page header/footer. Could also use \thispagestyle{empty}. *********
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}

% ********* Question formatting -- will be made more robust and have point tracking added in the future. *********
\newcounter{question}

\NewDocumentCommand{\question}{O{} m}{%
  \refstepcounter{question}
  \vspace{1em}
  \noindent
  \textbf{Question \thequestion}
  \IfValueT{#1}{\textbf{ (#1 points)}}:
  #2
  \par\vspace{0.5em}
}

% ********* Set default enumerate to letters for question subparts. Eventually will have parts environment. *********
\renewcommand{\labelenumi}{(\alph{enumi})}

% ********* Create lookup of page points from the gradetable macro. *********
\newcommand{\thepagepoints}{0}

\newcommand{\setpagepointvalue}[2]{%
  \expandafter\gdef\csname pagepoints@#1\endcsname{#2}%
}

\newcommand{\getpagepoints}[1]{%
  \ifcsname pagepoints@#1\endcsname
    \csname pagepoints@#1\endcsname
  \else
    0
  \fi
}

% ---------- Grading Table (AUTO-LINKED TO PAGE POINTS CURRENTLY) ----------
\usepackage{array}

\newcounter{gradetablepage}
\newcounter{gradetotal}

\newcommand{\gradetable}[1]{%
  \setcounter{gradetablepage}{0}%
  \setcounter{gradetotal}{0}%
  \renewcommand{\arraystretch}{1.5}
  \begin{tabular}{|c|c|c|}
    \hline
    \textbf{Page} & \textbf{Points} & \textbf{Earned} \\
    \hline
    \gradetableaux#1,\relax
    \textbf{Total} & \textbf{\thegradetotal} & \\ \hline
    \multicolumn{2}{|c|}{Final Mark:} & \\ \hline
  \end{tabular}
}

\def\gradetableaux#1,#2\relax{%
  \def\temp{#1}%
  \ifx\temp\empty
    % skip empty (handles trailing comma)
  \else
    \stepcounter{gradetablepage}%
    \addtocounter{gradetotal}{#1}%
    % Store page -> points mapping
    \setpagepointvalue{\thegradetablepage}{#1}%
    \thegradetablepage & #1 & \\ \hline
  \fi
  \ifx\relax#2\relax
  \else
    \gradetableaux#2\relax
  \fi
}

% ---------- Build Exam Cover Page ----------
\newcommand{\makeexamcover}[1]{%
\section*{\examtitle}
\setcounter{page}{0}
{\centering
\coursename\par
\examdate\par}
\vspace{2\baselineskip}
\hfill Student Name: \rule{.4\textwidth}{.4pt}\par
\vspace{2\baselineskip}
\textbf{Instructions:}
\instructions
\vfill
\begin{multicols}{2}
{
  \rule{0cm}{6\baselineskip}
  \rule{3cm}{0cm}
  \Large\textbf{Do your best!}\par
}
\columnbreak
\hfill
% Example grading table: pages worth 10, 15, 20 points
\gradetable{#1}
\vfill
\end{multicols}
\newpage
% Make footer dynamic
\fancyfoot[R]{Earned this page: \fbox{\rule{3\baselineskip}{0cm}\rule[-.5\baselineskip]{0cm}{1.5\baselineskip}} / \getpagepoints{\thepage}}
\fancyhead[R]{Page \thepage~of \pageref*{LastPage}}
\fancyhead[L]{\examtitle}
}
