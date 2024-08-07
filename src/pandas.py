import pandas as pd

def compute_2D(df_all, d1: str, d2: str, d3: str=None, method='sum', total=False, mean=False):
    '''
    Returns df where rows are d1 uniques, columns are d2 uniques, cells are d2-by-d1-count or d3 analysis (if provided)

    Args:
    - df_all: df with full data
    - d1: primary categorical column - set to output row index.
    - d2: secondary categorical column - set to output columns.
    - d3: optional tertiary category whose value will be analysed using the passed method
    - method: 'sum', 'mean', 'min', 'max' or 'nunique'. Only use where d3 != None.
    '''
    df = pd.DataFrame(index=df_all[d1].drop_duplicates().sort_values())

    # iterate over each d2 unique value:
    for cat in df_all[d2].drop_duplicates().sort_values():
        if d3 is None:
            vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1]).size()
        elif d3 is not None:
            if method=='sum':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].sum()
            elif method=='mean':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].mean()
            elif method=='nunique':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].nunique()
            elif method=='min':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].min()
            elif method=='max':
                vals_by_d1 = df_all.loc[df_all[d2]==cat].groupby([d1])[d3].max()
        
        # rename vals_by_d1 and merge into df
        ser = pd.Series(vals_by_d1)
        ser.name = 'None' if cat==None else cat
        df = pd.merge(df, ser, how='left', left_index=True, right_index=True,)
    
    df = df.fillna(0)
    if total == True:
        df['total'] = df.sum(axis=1)
    if mean == True:
        df['mean'] = df.mean(axis=1)
    return df

def compute_2D_multiple_d2(df_all, d1: str, d2: list, d3: str=None, method='sum', total=False, mean=False):
    '''
    Returns df where rows are d1 uniques, columns are d2 uniques, cells are d2-by-d1-count or d3 analysis (if provided).
    Unlike compute_2D where d2 is one column with multiple categories, here, d2 is a list of columns, with 0/1 value type.

    Args:
    - df_all: df with full data
    - d1: primary categorical column - set to output row index.
    - d2: list of secondary categorical columns - set to output columns.
    - d3: optional tertiary category whose value will be analysed using the passed method
    - method: 'sum' or 'mean'. If d3 is present, also 'nunique'
    '''
    df = pd.DataFrame(index=df_all[d1].drop_duplicates().sort_values())

    # iterate over each d2 columns:
    for cat in d2:
        if d3 is None:
            if method=='sum':
                vals_by_d1 = df_all.groupby([d1])[cat].sum()
            elif method=='mean':
                vals_by_d1 = df_all.groupby([d1])[cat].mean()
        elif d3 is not None:
            if method=='sum':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].sum()
            elif method=='mean':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].mean()
            elif method=='nunique':
                vals_by_d1 = df_all.loc[df_all[cat]==1].groupby([d1])[d3].nunique()
        
        # rename vals_by_d1 and merge into df
        vals_by_d1.name = 'None' if cat==None else cat
        df = pd.merge(df, vals_by_d1, how='left', left_index=True, right_index=True,)
    
    df = df.fillna(0)
    if total == True:
        df['total'] = df.sum(axis=1)
    if mean == True:
        df['mean'] = df.mean(axis=1)
    return df

def sum_others(series: pd.Series, top: int):
    '''
    Returns top n elements of a series and sum everything else to index 'Others'
    '''
    tail_len = len(series) - top
    out = series.head(top)
    out.loc['Others'] = series.tail(tail_len).sum()
    return out