# FUNCTION TO MODIFY HSPF MODEL PARAMETERS FROM CSV
# Ryan Shojinaga, Water Quality Analyst, NRS3, Oregon DEQ
# shojinaga.ryan@deq.state.or.us, 503-229-5777

# Lampert, David. (2015). PyHSPF: Data integration software for hydrologic and
#   water quality modeling. 

def modify_parameters(modelInName, modelOutName):

    # LOAD MODEL
    if not os.path.isfile(modelInName):
        print('Missing model file; re-run build_siletz_model.py')
        raise

    with open(modelInName, 'rb') as f: hspfmodel = pickle.load(f)

    # READ IN THE ADJUSTED PARAMETERS FROM CSVs
    csvFiles = ['\\calib\\pwat.csv',
                '\\calib\\mint.csv',
                '\\calib\\lzet.csv',
                '\\calib\\rtks.csv']

    modPars = []

    for i in range(0, len(csvFiles)):

        csvFile = os.path.abspath(os.path.curdir) + csvFiles[i]

        temp = read_csv_to_list(csvFile)

        modPars.append(temp)

    # MODIFY THE PARAMETERS IN THE MODEL FROM THE CSV PARAMETERS
    for i in range(0, len(hspfmodel.perlnds)):

        # MODIFY THE VARIABLE LOWER ZONE ET SWITCH IN PWAT-PARM1
        hspfmodel.perlnds[i].set_pwat_parms('Metric', VLE = 1)
    
        # Modify PWAT-PARMS first 
        hspfmodel.perlnds[i].LZSN   = modPars[0][i][0] # A. Lower zone storage
        hspfmodel.perlnds[i].INFILT = modPars[0][i][1] # B. Infiltration rate 
        hspfmodel.perlnds[i].LSUR   = modPars[0][i][2] # C. Overland slope
        hspfmodel.perlnds[i].AGWRC  = modPars[0][i][3] # D. Groundwater recess 
        hspfmodel.perlnds[i].DEEPFR = modPars[0][i][4] # E. Act -> Inact GW fr
        hspfmodel.perlnds[i].BASETP = modPars[0][i][5] # F. Base fract for ET
        hspfmodel.perlnds[i].AGWETP = modPars[0][i][6] # F. Active GW ET para
        hspfmodel.perlnds[i].UZSN   = modPars[0][i][7] # H. Upper zone storage
        hspfmodel.perlnds[i].INTFW  = modPars[0][i][8] # J. Interflow parameter
        hspfmodel.perlnds[i].IRC    = modPars[0][i][9] # K. Interflow recession

        # Modify monthly interception
        monInt = modPars[1][i]
        hspfmodel.perlnds[i].set_monthly(name = 'INTERCEP', values = monInt)

        # Modify monthly lower zone ET
        monET = modPars[2][i]
        hspfmodel.perlnds[i].set_monthly(name = 'LZETPARM', values = monET)

        # PERLND SEDIMENT
        # SED-PARM1, General flags
        hspfmodel.perlnds[i].set_sed_parm1(CRV = 1, VSIS = 0, SDOP = 1)
        # SED-PARM2, Sediment transport
        hspfmodel.perlnds[i].KRER       = 0.150         # Soil detachment coeff
        hspfmodel.perlnds[i].JRER       = 2.000         # Soil detachment expon
        hspfmodel.perlnds[i].AFFIX      = 0.070         # Daily detached sed -
        # SED-PARM3, Sediment transport
        hspfmodel.perlnds[i].KSER       = 1.100         # Sed washoff coeff
        hspfmodel.perlnds[i].JSER       = 2.000         # Sed washoff expnt
        # SED-STOR, Sediment initial value of detached sediment
        hspfmodel.perlnds[i].DETS       = 0.100         # Sed store init
        # FIXED VALUES --------------------------------------------------------
        hspfmodel.perlnds[i].NVSI       = 0.000         # Sed deposition rate
        hspfmodel.perlnds[i].KGER       = 0.000         # Soil scour coeff
        hspfmodel.perlnds[i].JGER       = 1.000         # Soil scour expnt
        # FIXED VALUES --------------------------------------------------------

    # MODIFY PARAMETERS FOR RCHRES HYDR-PARM2 ROUTING PARAMETER Ks
    for i in range(0, len(hspfmodel.rchreses)):

        # Hydraulics
        hspfmodel.rchreses[i].KS = modPars[3][i][0]
        
        # Sediment
        hspfmodel.rchreses[i].DB50      = 0.010         # Particle size D50   
        hspfmodel.rchreses[i].POR       = 0.200         # Substrate porosity

        # Sand characteristics
        hspfmodel.rchreses[i].Wsand     = 0.500         # Fall velocity
        hspfmodel.rchreses[i].KSAND     = 0.100         # Sandload coefficient
        hspfmodel.rchreses[i].EXPSND    = 2.000         # Sandload exponent
        # Silt characteristics
        hspfmodel.rchreses[i].Wsilt     = W      # Fall velocity (mm/s)
        hspfmodel.rchreses[i].TAUCDsilt = TAUCD  # Critical depos shear (kg/m2)
        hspfmodel.rchreses[i].TAUCSsilt = TAUCS  # Critical scour shear (kg/m2)
        hspfmodel.rchreses[i].Msilt     = M      # Silt erobability (kg/m2/day)
        # Clay characteristics
        hspfmodel.rchreses[i].Wclay     = W      # Fall velocity (mm/s)
        hspfmodel.rchreses[i].TAUCDclay = TAUCD  # Critical depos shear (kg/m2)
        hspfmodel.rchreses[i].TAUCSclay = TAUCS  # Critical scour shear (kg/m2)
        hspfmodel.rchreses[i].Mclay     = M      # Clay erobability (kg/m2/day)
        # FIXED VALUES --------------------------------------------------------
        # Sediment characteristics
        hspfmodel.rchreses[i].Dsand     = 0.250      # Diameter (mm)
        hspfmodel.rchreses[i].Dsilt     = 0.050      # Diameter (mm)
        hspfmodel.rchreses[i].Dclay     = 0.010      # Diameter (mm)
        # Initial instream concentrations -- FIXED
        hspfmodel.rchreses[i].Sand      = 2.250         # Sand conc. (mg/L)   
        hspfmodel.rchreses[i].Silt      = 2.250         # Silt conc. (mg/L)   
        hspfmodel.rchreses[i].Clay      = 0.500         # Clay conc. (mg/L)   
        # Initial bed composition -- FIXED
        # Pakenham, A., 2009. Patterns of Sediment Accumulation in the Siletz 
        #    River Estuary, Oregon. Masters Thesis. Oregon State Univeristy
        hspfmodel.rchreses[i].FSand     = 0.450         # Sand bed fraction
        hspfmodel.rchreses[i].FSilt     = 0.450         # Silt bed fraction
        hspfmodel.rchreses[i].FClay     = 0.100         # Clay bed fraction
        # FIXED VALUES --------------------------------------------------------

    # PICKLE THE MODEL WITH A NEW NAME
    with open(modelOutName, 'wb') as f: pickle.dump(hspfmodel, f)
    something = 1 # Just to give an terminus to the 'with' in the previous line

def read_csv_to_list(csvFil):

    with open(csvFil) as file:
    
        readTables = csv.reader(file, delimiter = ',')

        temp = []
    
        for row in readTables:

            temp.append(row)
    
    temp.pop(0) # Deletes the header row

    lists = 0

    for i in temp:

        temp[lists] = [float(row) for row in temp[lists]]

        lists += 1

    return(temp)

