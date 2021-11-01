import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency



def coef(df,var1,var2):
    l=len(df[var1].unique())
    c=len(df[var2].unique())
    N=df.shape[0]
    tableau_contingence=pd.DataFrame(pd.crosstab(df[var1],df[var2],margins = False))
    chi2,p= chi2_contingency(tableau_contingence)[0:2]
    mini = min(l-1,c-1)
    V=np.sqrt(chi2/(N*mini))
    T=np.sqrt(chi2/(N*np.sqrt((l-1)*(c-1))))
    return p,V,T

def _color_red_or_green(val,s=0.05):
    color = 'red' if val>s else 'green'
    return 'color: %s' % color

def Between_quali(df,noms_var,method):
    m=len(noms_var)
    mat=np.zeros((m,m))
    
    if method=="chi2":
        for i in range(m):
            for j in range(m):
                mat[i,j]=coef(df,noms_var[i],noms_var[j])[0]
        df1=pd.DataFrame(mat,columns=noms_var,index=noms_var)
        return df1.style.applymap(_color_yellow_or_green)
    if method=="V":
        for i in range(m):
            for j in range(m):
                mat[i,j]=coef(df,noms_var[i],noms_var[j])[1]
        df1=pd.DataFrame(mat,columns=noms_var,index=noms_var)
        a=sns.heatmap(df1[df1>=0.5],cmap="viridis",vmax=1, vmin=0.0, linewidths=0,annot=True, annot_kws={"size":8},square=True)
        return a
    
    if method=="T":
        for i in range(m):
            for j in range(m):
                mat[i,j]=coef(df,noms_var[i],noms_var[j])[2]
        df1=pd.DataFrame(mat,columns=noms_var,index=noms_var)
        a=sns.heatmap(df1[df1>=0.5],cmap="viridis",vmax=1.0, vmin=0.0, linewidths=0,annot=True, annot_kws={"size":8},square=True)
        return a
