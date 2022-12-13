from PIL import Image
import math
from fpdf import FPDF
from scipy.interpolate import interp1d

def main():
    print("Enter The Required Data : -")
    main.fck=int(input("Enter The Grade of Concrete : "))
    main.fy=int(input("Enter The Grade of Steel : "))
    #main.ExposureCondition=str(input("Enter The Exposure Condtion : "))
    main.LiveLoadInput=int(input("Enter The Magnitude of Live Load (kN/m^2): "))
    main.WidthOfSupport=int(input("Enter Width of Support (mm): "))
    main.SpanOfSlabx=float(input("Dimension in x Direction (m): "))
    main.SpanOfSlaby=float(input("Dimension in y Direction (m): "))
    main.StartinCondition=main.SpanOfSlaby/main.SpanOfSlabx
    if main.StartinCondition==2 or main.StartinCondition > 2:
        print("* This can be designed as one way slab *")
            #1. TrialDepth
        main.TypeOfSupport=str(input("Type of Support (Cantilever / Simply Supported / Continuous) : "))
        if main.TypeOfSupport==("Cantilever"):
            main.LByDRatio=7
        elif main.TypeOfSupport==("Simply Supported") or main.TypeOfSupport==("simply supported") or main.TypeOfSupport==("SIMPLY SUPPORTED"):
            main.LByDRatio=20
            #ShowThePercentageSteelTabel
            im = Image.open(r"E:\VIIT\Semister 5\SDD 1\Assets\%steelTable.jpg") 
            im.show()
            main.percentageSteel=float(input("Enter The Percentage of Tension Reinforcement : "))
            main.fsTrial=0.58*main.fy
            #ShowTheGraph
            print("fs = " + str(main.fsTrial))
            im = Image.open(r"E:\VIIT\Semister 5\SDD 1\Assets\mfChart.jpg")
            im.show()
            main.Alpha1=float(input("Enter The Value of Alpha 1 : "))
            main.d=(main.SpanOfSlabx/((main.LByDRatio)*main.Alpha1))*1000
            print("Effective Depth of Slab (d) : " + str(round(main.d, 3)) + " mm (Recommended)")
            main.d=float(input("Enter Effective Depth of Slab (d) (mm): "))
            main.barDiameter=int(input("Enter The Bar Diameter (mm): "))
            main.exposureCondition=str(input("Enter The Exposure Condition : "))
            im = Image.open(r"E:\VIIT\Semister 5\SDD 1\Assets\exposureCondition.jpg") 
            im.show()
            main.clearCover=int(input("Enter Clear Cover : "))
            main.overallDepth=main.d+main.clearCover+(main.barDiameter/2)
            print("Overall Depth (D) : " + str(main.overallDepth) + " mm (Recommended)")
            main.overallDepth=int(input("Enter Overall Depth (D) (mm) : "))
           
            #2. EffectiveSpan
            main.centreToCentreDist=(1000*main.SpanOfSlabx)
            main.clearSpan=((1000*main.SpanOfSlabx)-main.WidthOfSupport)+main.d
            main.effectiveSpan=min(main.centreToCentreDist, main.clearSpan)
            print("Effective Span " + str(main.effectiveSpan) + " mm")
            
            #3. LoadCalculation
            print("Assume 1m Strip of Slab, i.e. b = 1m = 1000mm")
            main.b=1
                #DeadLoad
            main.SelfWeight=(25*main.b*(main.overallDepth)/1000)
            main.FloorFinish=1
            main.DeadLoad=main.SelfWeight+main.FloorFinish
            print("Dead Load " + str(main.DeadLoad) + " kN/m")
                #LiveLoad
            main.LiveLoad=main.LiveLoadInput*main.b
            print("Live Load " + str(main.LiveLoad) + " kN/m")
                #TotalLoad
            main.TotalLoad=main.DeadLoad+main.LiveLoad
            main.TotalUltimateLoad=1.5*main.TotalLoad
            print("Total Ultimate Load : " + str(main.TotalUltimateLoad) + " kN/m")
            
            
            #4. UltimateMoment
            main.Mu=(main.TotalUltimateLoad*(main.effectiveSpan/1000)**2)/8
            print("Ultimate Moment : " + str(main.Mu) + " kN.m")
            main.Vu=(main.TotalUltimateLoad*(main.effectiveSpan/1000))/2
            print("Ultimate Shear Force : " + str(main.Vu) + " kN")

            #5. MomentCarryingCapacity
            main.RuMax=0.138*main.fck
            main.MurMax=(main.RuMax*main.b*(main.d)**2)/10**3
            if main.MurMax >= main.Mu:
                print("Moment Carrying Capacity (MurMax) : " + str(main.MurMax) + " kN.m")
                print("Ok")
            else:
                print("Not Ok")
                main()
            
            #6. CalculationOfMainSteelAst
            #main.Ast0=((0.5*main.fck)/main.fy)*(1-((1-((4.6*main.Mu*10**6)/main.fck*main.b*(main.d**2)))**(1/2)))*main.b*main.d
            main.Ast1=((0.5*main.fck)/main.fy)
            print(main.Ast1)
            main.Ast2=1-((4.6*main.Mu*10**6)/(main.fck*1000*(main.d**2)))
            print(main.Ast2)
            main.Ast3=1-((main.Ast2)**(1/2))
            
            print(main.Ast3)
            main.Ast=(main.Ast1*main.Ast3)*(main.b*1000)*main.d
            main.printValueAstCalculated=main.Ast
            print("Ast = " + str(main.Ast) + " mm^2")
            main.AstMin=(0.12/100)*((main.b*1000)*main.overallDepth)
                #CheckForAst
            if main.Ast>=main.AstMin:
                print("OK")
            elif main.Ast<main.AstMin:
                main.Ast=main.AstMin
            else: 
                print("Error")
                #AreaOfOneBar
            
            print("Ast = " + str(main.Ast) + " mm^2")
            main.AreaOfOneBar=((math.pi)/4)*(main.barDiameter**2)
            print("ast = " + str(main.AreaOfOneBar) + " mm^2")
                #Spacing
            main.S=1000*(main.AreaOfOneBar/main.Ast)
                #CheckForSpacing
            main.spacingCheck1=3*main.d
            main.spacingCheck2=300
            main.SpacingMin=min(main.S , main.spacingCheck1 , main.spacingCheck2)
            print("Spacing Recommended : " + str(main.SpacingMin) + " mm")
            if main.SpacingMin != main.spacingCheck1 or main.SpacingMin != main.spacingCheck2:
                main.Spacing=main.SpacingMin
            elif main.SpacingMin==main.S:
                main.Spacing=int(input("Enter Spacing (mm) : "))
            else:
                main.Spacing=main.S
            print("Provide " +str(main.barDiameter) + " mm @ " + str(main.Spacing) + " mm c\c")
            main.AstProvided=1000*(main.AreaOfOneBar/main.Spacing)
            print("Ast Provided = " +str(main.AstProvided) + " mm^2")

            #7. CalculationForDistributionSteel
            main.distributionDia=int(input("Enter The Bar Diameter For Distribution Steel : "))
            print("Steel Grade : - ")
            print("1. Mild Steel")
            print("2. HYSD Steel")
            main.distributionDiaType=int(input("Select Steel Grade : "))
            if main.distributionDiaType==1:
                print("Mild Steel")
                main.Asd=(0.15/100)*(main.b*1000)*main.overallDepth
            elif main.distributionDiaType==2:
                print("HYSD Steel")
                main.Asd=(0.12/100)*(main.b*1000)*main.overallDepth
            else: 
                print("Wrong Input !!!")
            print("Asd = " +str(main.Asd))
            main.asd=((math.pi)/4)*(main.distributionDia**2)
            print("asd = " +str(main.asd))
                #SpacingForDistributionSteel
            main.SpacingD=1000*(main.asd/main.Asd)
            main.SpacingDCheck1=5*main.d
            main.SpacingDCheck2=450
            main.SpacingDMin=min(main.SpacingD, main.SpacingDCheck1, main.SpacingDCheck2)
            print("Spacing = " + str(main.SpacingDMin) + " mm (Recommended)")
            if main.SpacingDMin != main.SpacingDCheck1 or main.SpacingDMin != main.SpacingDCheck2:
                main.SpacingDMin=int(input("Enter Spacing For Distribution Steel (mm): "))
                main.SpacingD=main.SpacingDMin
            else:
                main.SpacingD=main.SpacingDMin
            print ("Provide " + str(main.distributionDia) + " @ " +str(main.SpacingD) + " mm c/c")

            #8. CheckForDeflection
            main.PercentageSteelPt=100*(main.AstProvided/((main.b*1000)*main.d))
            print("Check for Deflection : - ")
            print("Percentage Steel = " + str(main.PercentageSteelPt) + " %")
                #CalculateStressInSteel
            main.fs2=(0.58*main.fy)*(main.Ast/main.AstProvided)
            print("fs =" + str(main.fs2))
            #ShowImage
            im = Image.open(r"E:\VIIT\Semister 5\SDD 1\Assets\mfChart.jpg")
            im.show()
            main.Alpha2=float(input("Enter The Value of Alpha 1 : "))
            main.dreq=(main.SpanOfSlabx*1000)/(main.LByDRatio*main.Alpha2)
            if main.dreq<=main.d:
                print("As dreq is <= dassumed, check is satisfied, Ok")
            else:
                print("As dreq is Not <= dassumed, check not satisfied")
            print("dreq = " + str(main.dreq) + " mm")

            #9. Check For Shear 
            print("Design Shear Force (Vu): " +str(main.Vu) + " kN")
                #CalculateMaximumAllowableShearInConcrete
            im = Image.open(r"E:\VIIT\Semister 5\SDD 1\Assets\MaxShearStress.jpg")
            im.show()
            main.TauCMax=float(input("Enter The Value of τcmax : "))
            main.VucMax=main.TauCMax*(main.b)*main.d
            if main.VucMax>=main.Vu:
                print("As VucMax is Greater Than Vu, Hence Ok")
            else:
                print("As VucMax is Not Greater Than Vu, Hence Not Ok")
            print(("VucMax = " +str(main.VucMax)) + " kN")
                #ShearStrengthOfConcrete(Vuc)
                    #ForTauC
            X = [0.15,0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00,2.25,2.50,2.75,3.00] # random x values
            Y = [0.28,0.36,0.48,0.56,0.62,0.67,0.72,0.75,0.79,0.81,0.82,0.82,0.82] # random y values
            # test value
            ValueOfTauC = main.PercentageSteelPt
            # Finding the interpolation
            TauC = interp1d(X, Y)
            print("Value of Y at x = {} is".format(ValueOfTauC),
                TauC(ValueOfTauC))
            main.TauC=TauC(ValueOfTauC)
                    #ForK
            if main.overallDepth<=150:
                main.k=1.30
            elif main.overallDepth>=300:
                main.k=1.00
            else:
                Depth=[275.0, 250.0, 225.0, 200.0, 175.0]
                Kvalue=[1.05, 1.10, 1.15, 1.20, 1.25]
                interpolate_Kvalue = main.overallDepth
                y_interp = interp1d(Depth, Kvalue)
                main.k=interpolate_Kvalue
            print(main.k)
            print(main.TauC)
                #CalculatingVuc
            main.Vuc=main.k*main.TauC*(main.b)*main.d
            print(main.Vuc)
            if main.Vuc>=main.Vu:
                print("Check Satisfied, Hence Ok")
            else:
                print("Check not Satisfied, Hence Not Ok")

            #10. CheckForDevelopmentLength
            main.ld=(0.87*main.fy*main.barDiameter)/(4*1.92)
            print("Ld = " + str(main.ld) + " mm")
            main.m1=main.MurMax/2
            main.l0=(main.WidthOfSupport/2)-main.clearCover+(3*main.barDiameter)
            if main.l0<main.d or main.l0<(12*main.barDiameter):
                print("Lo = " + str(main.l0) + " mm")
            else: 
                main.l0=max(main.d, (12*main.barDiameter))
                print("Lo = " + str(main.l0) + " mm")
            #Check for development Length
            if main.ld<(((1.3*main.m1*10**6)/(main.Vu*10**3))+main.l0):
                print("As Ld < (1.3M1/Vu)+l0, Check Satisfied, Hence Ok")
            else:
                print("As Ld > (1.3M1/Vu)+l0, Check Not Satisfied, Hence Not Ok")
            raw_input=str(input('............Design Completed............'))
            NewSlabDesign=str(input("Do You Want To Design Another Slab ? : "))
            if NewSlabDesign==("yes") or NewSlabDesign==("YES") or NewSlabDesign==("Yes"):
                main()
            elif NewSlabDesign==("NO") or NewSlabDesign==("no") or NewSlabDesign==("No"):
                print("")
            DesignInPDF=str(input("Do you want PDF Copy of Design (Yes/No) : "))
            if DesignInPDF==("yes") or DesignInPDF==("YES") or DesignInPDF==("Yes"):
                print("Generating PDF Output........")
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                #pdf.set_font("Arial" , size = 15)
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt = "Design of RC One Way Slab", ln = 1, align = 'C'),
                pdf.cell(200, 10, txt= "Data :- ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Concrete - M" +str(main.fck) , ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Steel - Fe"+ str(main.fy) , ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Live Load - " + str(main.LiveLoadInput) + " kN", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Width of Support - " + str(main.WidthOfSupport) + " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Dimension of Slab - " + str(main.SpanOfSlabx) +" m" + " x " + str(main.SpanOfSlaby)+" m", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Exposure Condition - "+ str(main.exposureCondition), ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "------------------------------------------------------------------------------------------------------------ ", ln= 1, align= 'C'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "1. Type of Support :- Simply Supported", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Effective Depth (d) = " +str(main.d) + " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Overall Depth (D) = " +str(main.overallDepth) + " mm", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "2. Effective Span :- ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Effective Span =  " + str(main.effectiveSpan) + " mm", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "3. Load Calculation :- ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Dead Load = " + str(main.DeadLoad) + " kN/m", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Live Load =  " + str(main.LiveLoad) + " kN/m", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Total Ultimate Load (Wu) = " + str(main.TotalUltimateLoad) + " kN/m", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "4. Ultimate Moment (Mu) & Shear Force (Vu)", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Ultimate Moment (Mu) = " + str(round(main.Mu, 3)) + " kN.m", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Ultimate Shear Force (Vu) = " + str(round(main.Vu, 3)) + " kN", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "5. Moment Carrying Capacity :- ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Murmax = " + str(round(main.MurMax,3)) + " kN.m", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "6. Calculatoin of Main Steel (Ast) :- ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Ast = "+ str(round(main.printValueAstCalculated, 3)) + " mm^2", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Astmin = "+ str(round(main.AstMin, 3))+ " mm^2", ln= 1, align= 'L'),
                if main.printValueAstCalculated<main.AstMin:
                    pdf.cell(200, 10, txt= "    As Calculated Ast is < Astmin Provide, Ast Min", ln= 1, align= 'L'),
                elif main.printValueAstCalculated<main.AstMin:
                    pdf.cell(200, 10, txt= "    As Calculated Ast is > Astmin Provide, Ast", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Bar Diameter = " +str(main.barDiameter)+ " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Spacing (S) = " + str(round(main.Spacing,0)) + " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Provide " +str(main.barDiameter) + " mm @ " + str(main.Spacing) + " mm c\c", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Astprovided = " +str(round(main.AstProvided,3)) + " mm^2", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "7. Calculation For Distribution Steel (Astd) :-", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                if main.distributionDiaType==1:
                    pdf.cell(200, 10, txt= "    Steel For Astd = Mild Steel", ln= 1, align= 'L'),
                elif main.distributionDiaType==2:
                    pdf.cell(200, 10, txt= "    Steel For Astd = HYSD Steel", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Bar Diameter = " + str(main.distributionDia) + " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Astd = " + str(main.Asd)+ " mm^2", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Spacing (S) = " +str(main.SpacingD) + " mm", ln= 1, align= 'L'),
                if main.distributionDiaType==1:
                    pdf.cell(200, 10, txt= "    Provide " + str(main.distributionDia) + " Mild Steel Bars" + " @ " +str(main.SpacingD) + " mm c/c", ln= 1, align= 'L'),
                elif main.distributionDiaType==2:
                    pdf.cell(200, 10, txt= "    Provide " + str(main.distributionDia) + " HYSD Steel Bars" + " @ " +str(main.SpacingD) + " mm c/c", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "8. Check For Deflection ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    dreq = " + str(main.dreq) + " mm", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    dassumed = " + str(main.d) + " mm", ln= 1, align= 'L'),
                if main.dreq<=main.d:
                    pdf.cell(200, 10, txt= "    As dreq is less than equal dassumed, Hence Ok ", ln= 1, align= 'L'),
                else:
                    
                    pdf.cell(200, 10, txt= "    As dreq is Not less than equal dassumed, Hence Not Ok ", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "9. Check For Shear :-", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Vu = " +str(round(main.Vu,3)) + " kN", ln= 1, align= 'L'),
                pdf.cell(200, 10, txt= "    Vucmax = " +str(round(main.VucMax,3))+ " kN", ln= 1, align= 'L'),
                if main.VucMax>=main.Vu:
                    
                    pdf.cell(200, 10, txt= "    As Vucmax is greater than equal to Vu, Hence Ok", ln= 1, align= 'L'),
                else:
                    
                    pdf.cell(200, 10, txt= "    As Vucmac is not greater than equal to Vu, Hence Not Ok", ln= 1, align= 'L'),
                pdf.set_font("Arial" , 'B', 15)
                pdf.cell(200, 10, txt= "10. Check For Development Length :-", ln= 1, align= 'L'),
                pdf.set_font("Arial" , size = 15)
                pdf.cell(200, 10, txt= "    Ld = " + str(round(main.ld, 3)) + " mm", ln= 1, align= 'L'),
                if main.ld<(((1.3*main.m1*10**6)/(main.Vu*10**3))+main.l0):
                    pdf.cell(200, 10, txt= "    Lo = " + str(round((((1.3*main.m1*10**6)/(main.Vu*10**3))+main.l0),3)) + " mm", ln= 1, align= 'L')
                    pdf.cell(200, 10, txt= "    As Ld < (1.3M1/Vu)+lo, Check Satisfied, Hence Ok", ln= 1, align= 'L'),  
                else:
                    pdf.cell(200, 10, txt= "    Lo = " + str(round((((1.3*main.m1*10**6)/(main.Vu*10**3))+main.l0),3)) + " mm", ln= 1, align= 'L')
                    pdf.cell(200, 10, txt= "    As Ld > (1.3M1/Vu)+lo, Check Not Satisfied, Hence Not Ok", ln= 1, align= 'L'),  
                pdf.output("Design of RC One Way Slab.pdf")
            else:
                raw_input=int(input("......."))
        elif main.TypeOfSupport==("Continuous"):
            main.LByDRatio=26
        else: 
            print("Error")
    else:
        print("* This is a Two way slab *")
        exit()
main()