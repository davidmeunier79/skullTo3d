"""
    Gather all full pipelines

"""
import nipype.interfaces.utility as niu
import nipype.pipeline.engine as pe

from nipype.interfaces.fsl.maths import (
    DilateImage, ErodeImage, ApplyMask, UnaryMaths, Threshold)

from nipype.interfaces.fsl.utils import RobustFOV
from nipype.interfaces.fsl.preprocess import FAST


from nipype.interfaces.niftyreg.reg import RegAladin

from macapype.utils.utils_nodes import NodeParams

from nodes.skull import keep_gcc, wrap_nii2mesh, pad_zero_mri

from macapype.utils.misc import parse_key


def create_skull_petra_pipe(name="skull_petra_pipe", params={}):

    # creating pipeline
    skull_segment_pipe = pe.Workflow(name=name)

    # Creating input node
    inputnode = pe.Node(
        niu.IdentityInterface(fields=['petra', 'brainmask', 'debiased_T1',
                                      'indiv_params']),
        name='inputnode'
    )

    # output node
    outputnode = pe.Node(
        niu.IdentityInterface(
            fields=['head_mask', 'skull_mask']),
        name='outputnode')

    # pad_T1_debiased
    pad_T1_debiased = NodeParams(
        interface=niu.Function(
            input_names=["img_file", "pad_val"],
            output_names=["img_padded_file"],
            function=pad_zero_mri),
        params=parse_key(params, "pad_T1_debiased"),
        name="pad_T1_debiased")

    skull_segment_pipe.connect(inputnode, "debiased_T1",
                               pad_T1_debiased, "img_file")

    # pad_brainmask
    pad_brainmask = NodeParams(
        interface=niu.Function(
            input_names=["img_file", "pad_val"],
            output_names=["img_padded_file"],
            function=pad_zero_mri),
        params=parse_key(params, "pad_brainmask"),
        name="pad_brainmask")

    skull_segment_pipe.connect(inputnode, "brainmask",
                               pad_brainmask, "img_file")

    # align_petra_on_T1
    align_petra_on_T1 = pe.Node(interface=RegAladin(),
                                name="align_petra_on_T1")

    skull_segment_pipe.connect(inputnode, "petra",
                               align_petra_on_T1, "flo_file")

    skull_segment_pipe.connect(pad_T1_debiased, "img_padded_file",
                               align_petra_on_T1, "ref_file")

    # fast_petra ####### [okey][json]
    fast_petra = NodeParams(interface=FAST(),
                            params=parse_key(params, "fast_petra"),
                            name="fast_petra")

    # fast_petra.inputs.args = "-l 3"
    # fast_petra.inputs.output_biascorrected = True
    # fast_petra.inputs.output_biasfield = True

    skull_segment_pipe.connect(align_petra_on_T1, "res_file",
                               fast_petra, "in_files")

    # head_mask ####### [okey][json]
    head_mask = NodeParams(interface=Threshold(),
                           params=parse_key(params, "head_mask"),
                           name="head_mask")

    # head_mask.inputs.thresh = 800.0

    skull_segment_pipe.connect(fast_petra, "restored_image",
                               head_mask, "in_file")

    # head_mask_binary ####### [okey]
    head_mask_binary = pe.Node(interface=UnaryMaths(),
                               name="head_mask_binary")

    head_mask_binary.inputs.operation = 'bin'
    head_mask_binary.inputs.output_type = 'NIFTI_GZ'

    skull_segment_pipe.connect(head_mask, "out_file",
                               head_mask_binary, "in_file")

    # head_mask_binary_clean1 ####### [okey]
    keep_gcc_head = pe.Node(
        interface=niu.Function(input_names=["nii_file"],
                               output_names=["gcc_nii_file"],
                               function=keep_gcc),
        name="keep_gcc_head")

    skull_segment_pipe.connect(head_mask_binary, "out_file",
                               keep_gcc_head, "nii_file")

    # head_dilate ####### [okey][json]
    head_dilate = NodeParams(interface=DilateImage(),
                             params=parse_key(params, "head_dilate"),
                             name="head_dilate")

    # head_dilate.inputs.operation = 'modal'
    # head_dilate.inputs.kernel_shape = 'boxv'
    # head_dilate.inputs.kernel_size = 5.0

    skull_segment_pipe.connect(keep_gcc_head, "gcc_nii_file",
                               head_dilate, "in_file")

    # head_fill
    head_fill = pe.Node(interface=UnaryMaths(),
                        name="head_fill")

    head_fill.inputs.operation = 'fillh'

    skull_segment_pipe.connect(head_dilate, "out_file",
                               head_fill, "in_file")

    # keep_gcc_head2 ####### [okey]
    keep_gcc_head2 = pe.Node(
        interface=niu.Function(
            input_names=["nii_file"],
            output_names=["gcc_nii_file"],
            function=keep_gcc),
        name="keep_gcc_head2")

    skull_segment_pipe.connect(head_fill, "out_file",
                               keep_gcc_head2, "nii_file")

    # head_erode ####### [okey][json]
    head_erode = NodeParams(interface=ErodeImage(),
                            params=parse_key(params, "head_erode"),
                            name="head_erode")

    skull_segment_pipe.connect(keep_gcc_head2, "gcc_nii_file",
                               head_erode, "in_file")

    # fast_petra_hmasked ####### [okey]
    fast_petra_hmasked = pe.Node(interface=ApplyMask(),
                                 name="fast_petra_hmasked")

    skull_segment_pipe.connect(fast_petra, "restored_image",
                               fast_petra_hmasked, "in_file")

    skull_segment_pipe.connect(head_erode, "out_file",
                               fast_petra_hmasked, "mask_file")

    # fast_petra_hmasked_thr ####### [okey][json]
    fast_petra_hmasked_thr = NodeParams(
        interface=Threshold(),
        params=parse_key(params, "fast_petra_hmasked_thr"),
        name="fast_petra_hmasked_thr")

    skull_segment_pipe.connect(fast_petra_hmasked, "out_file",
                               fast_petra_hmasked_thr, "in_file")

    # skull_gcc ####### [okey]
    skull_gcc = pe.Node(
        interface=niu.Function(
            input_names=["nii_file"],
            output_names=["gcc_nii_file"],
            function=keep_gcc),
        name="skull_gcc")

    skull_segment_pipe.connect(fast_petra_hmasked_thr, "out_file",
                               skull_gcc, "nii_file")

    # skull_gcc_dilated ####### [okey][json]
    skull_gcc_dilated = NodeParams(
        interface=DilateImage(),
        params=parse_key(params, "skull_gcc_dilated"),
        name="skull_gcc_dilated")

    skull_segment_pipe.connect(skull_gcc, "gcc_nii_file",
                               skull_gcc_dilated, "in_file")

    # skull_fill #######  [okey]
    skull_fill = pe.Node(interface=UnaryMaths(),
                         name="skull_fill")

    skull_fill.inputs.operation = 'fillh'

    skull_segment_pipe.connect(skull_gcc_dilated, "out_file",
                               skull_fill, "in_file")

    # skull_fill_erode ####### [okey][json]
    skull_fill_erode = NodeParams(interface=ErodeImage(),
                                  params=parse_key(params, "skull_fill_erode"),
                                  name="skull_fill_erode")

    # skull_fill_erode.inputs.kernel_shape = 'boxv'
    # skull_fill_erode.inputs.kernel_size = 7.0

    skull_segment_pipe.connect(skull_fill, "out_file",
                               skull_fill_erode, "in_file")

    # brainmask_res
    """
    brainmask_res = pe.Node(interface=RegResample(),
                            name="brainmask_res")
    brainmask_res.inputs.inter_val = 'NN'

    skull_segment_pipe.connect(pad_brainmask, "img_padded_file",
                               brainmask_res, "flo_file")

    skull_segment_pipe.connect(skull_fill_erode, "out_file",
                               brainmask_res, "ref_file")
    """

    # brainmask_res_dilated ####### [okey][json]
    brainmask_res_dilated = NodeParams(
        interface=DilateImage(),
        params=parse_key(params, "brainmask_res_dilated"),
        name="brainmask_res_dilated")

    skull_segment_pipe.connect(pad_brainmask, "img_padded_file",
                               brainmask_res_dilated, "in_file")

    # skull_segment_pipe.connect(brainmask_res, "out_file",
    # brainmask_res_dilated, "in_file")

    # skull_bmask ####### [okey]
    skull_bmask = pe.Node(interface=ApplyMask(),
                          name="skull_bmask")

    skull_segment_pipe.connect(skull_fill_erode, "out_file",
                               skull_bmask, "in_file")

    skull_segment_pipe.connect(brainmask_res_dilated, "out_file",
                               skull_bmask, "mask_file")

    # skull_bmask_cleaning ####### [okey]
    skull_bmask_cleaning = pe.Node(
        interface=niu.Function(input_names=["nii_file"],
                               output_names=["gcc_nii_file"],
                               function=keep_gcc),
        name="skull_bmask_cleaning")

    skull_segment_pipe.connect(skull_bmask, "out_file",
                               skull_bmask_cleaning, "nii_file")

    # skull_fov ####### [okey][json]
    skull_fov = NodeParams(interface=RobustFOV(),
                           params=parse_key(params, "skull_fov"),
                           name="skull_fov")

    skull_segment_pipe.connect(skull_bmask_cleaning, "gcc_nii_file",
                               skull_fov, "in_file")

    # mesh_skull #######
    mesh_skull = pe.Node(
        interface=niu.Function(input_names=["nii_file"],
                               output_names=["stl_file"],
                               function=wrap_nii2mesh),
        name="mesh_skull")

    skull_segment_pipe.connect(skull_fov, "out_roi",
                               mesh_skull, "nii_file")

    # creating outputnode #######
    outputnode = pe.Node(
        niu.IdentityInterface(
            fields=["skull_mask", "skull_stl", "head_mask"]),
        name='outputnode')

    skull_segment_pipe.connect(head_erode, "out_file",
                               outputnode, "head_mask")

    skull_segment_pipe.connect(mesh_skull, "stl_file",
                               outputnode, "skull_stl")

    skull_segment_pipe.connect(skull_fov, "out_roi",
                               outputnode, "skull_mask")

    return skull_segment_pipe
